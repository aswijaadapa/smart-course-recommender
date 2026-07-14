"""
ml_engine.py
------------
The Machine Learning core of the Smart Course Recommendation System.

Approach: Content-Based Filtering using TF-IDF + Cosine Similarity.

WHY TF-IDF?
Every course has text describing it (category, skills, tags, description).
TF-IDF (Term Frequency - Inverse Document Frequency) converts that text into
a numeric vector, weighting words by how important they are:
  - Term Frequency: how often a word appears in a course's text (more = more relevant)
  - Inverse Document Frequency: words that appear in almost every course
    (like "the", "course", "learn") get pushed DOWN in importance, while
    distinctive words (like "kubernetes", "cryptography") get pushed UP.
This means two courses that share rare, meaningful words (e.g. "Django",
"REST APIs") are considered more similar than two that only share common
filler words.

WHY COSINE SIMILARITY?
Once every course (and the user's profile) is represented as a TF-IDF
vector, we need a way to measure how "close" two vectors are. Cosine
similarity measures the angle between two vectors rather than their
magnitude/length. This matters here because course descriptions vary a lot
in length — a short course description and a long one can still be about
the exact same topic. Cosine similarity correctly says they're similar
based on *direction* (word pattern), not penalizing the shorter one for
having fewer words. The result is a score from 0 (completely unrelated) to
1 (identical topic focus).

HOW THE RECOMMENDATION WORKS, STEP BY STEP:
1. Every course in the database is converted into one text blob combining
   its category, career domain, skills, tags, difficulty, and description.
2. TF-IDF is fit on all these course text blobs, producing a matrix where
   each row is a course and each column is a weighted word score.
3. The user's profile (skills + interests + career goal + experience level)
   is converted into the SAME kind of text blob and transformed using the
   SAME fitted TF-IDF vectorizer (never re-fit on a single user, since that
   would produce a vector in a completely different, incomparable space).
4. Cosine similarity is computed between the user's vector and every
   course vector.
5. Courses are sorted by similarity score, and the top N are returned.

ADVANTAGES of content-based filtering:
- Works from day one, even with only one user (no "cold start" problem
  like collaborative filtering has, which needs many users' behavior data).
- Recommendations are explainable — you can point to which words matched.
- No need to track other users' behavior/ratings to make it work.

LIMITATIONS:
- Only as good as the text description quality — vague tags/descriptions
  produce vague matches.
- Cannot discover totally novel interests outside what the user already
  described (unlike collaborative filtering, which can surprise you based
  on what similar OTHER users liked).
- Doesn't account for social proof (e.g. "94% of similar users loved this").
"""

import joblib
from pathlib import Path
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from courses.models import Course

VECTORIZER_PATH = Path(settings.ML_MODEL_DIR) / 'tfidf_vectorizer.joblib'
MATRIX_PATH = Path(settings.ML_MODEL_DIR) / 'tfidf_matrix.joblib'
COURSE_IDS_PATH = Path(settings.ML_MODEL_DIR) / 'course_ids.joblib'


def build_and_save_model():
    """
    Trains the TF-IDF model on all courses currently in the database and
    saves the vectorizer + resulting matrix + course ID order to disk with
    joblib, so the web app never has to retrain on every request.

    Run this any time the course dataset changes (new courses added,
    edited, or removed) — e.g. via:
        python manage.py train_model
    """
    courses = list(Course.objects.all())
    if not courses:
        raise ValueError("No courses found in the database. Load the dataset first.")

    course_ids = [c.id for c in courses]
    texts = [c.combined_text() for c in courses]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    Path(settings.ML_MODEL_DIR).mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(tfidf_matrix, MATRIX_PATH)
    joblib.dump(course_ids, COURSE_IDS_PATH)

    return len(courses)


def _load_model():
    if not (VECTORIZER_PATH.exists() and MATRIX_PATH.exists() and COURSE_IDS_PATH.exists()):
        raise FileNotFoundError(
            "Trained model files not found. Run 'python manage.py train_model' first."
        )
    vectorizer = joblib.load(VECTORIZER_PATH)
    tfidf_matrix = joblib.load(MATRIX_PATH)
    course_ids = joblib.load(COURSE_IDS_PATH)
    return vectorizer, tfidf_matrix, course_ids


def build_profile_text(skills, interests, career_goal, experience_level):
    """
    Builds the same style of text blob for a user's profile as
    Course.combined_text() does for a course, so both sides of the
    similarity comparison are constructed the same way.
    """
    return " ".join(filter(None, [skills, interests, career_goal, experience_level]))


def get_recommendations(skills, interests, career_goal, experience_level, top_n=8):
    """
    Returns a list of (Course, similarity_score) tuples, sorted by
    similarity score descending, for the given user profile inputs.
    """
    vectorizer, tfidf_matrix, course_ids = _load_model()

    profile_text = build_profile_text(skills, interests, career_goal, experience_level)
    user_vector = vectorizer.transform([profile_text])

    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Pair each course ID with its score, then sort descending
    scored = list(zip(course_ids, similarity_scores))
    scored.sort(key=lambda pair: pair[1], reverse=True)

    top_matches = scored[:top_n]

    # Fetch actual Course objects preserving the ranked order
    courses_by_id = Course.objects.in_bulk([cid for cid, _ in top_matches])
    results = []
    for course_id, score in top_matches:
        course = courses_by_id.get(course_id)
        if course:
            results.append((course, round(float(score), 4)))

    return results
