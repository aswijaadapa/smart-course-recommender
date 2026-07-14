# 🎓 Smart Course Recommendation System

A full-stack web application that recommends personalized online courses
using a **content-based Machine Learning recommender** (TF-IDF + Cosine
Similarity), built with **Django** and **Scikit-learn**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Folder Structure](#folder-structure)
4. [Installation Guide](#installation-guide)
5. [Dataset Description](#dataset-description)
6. [Algorithm Explanation](#algorithm-explanation)
7. [Features](#features)
8. [Future Enhancements](#future-enhancements)
9. [Resume / LinkedIn / GitHub Content](#resume--linkedin--github-content)

---

## Project Overview

Users register, fill in their **skills, interests, career goal, experience
level, weekly study hours, and preferred platform**, and receive the
**top 10 most relevant courses** out of a 200-course catalog, ranked by a
similarity score computed by a trained ML model — not hardcoded rules.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| ML | Pandas, NumPy, Scikit-learn (TF-IDF, Cosine Similarity), Joblib |
| Frontend | HTML, CSS, Bootstrap 5, vanilla JavaScript |
| Database | SQLite |
| Tools | VS Code, Git, GitHub |

---

## Folder Structure

```
smart-course-recommender/
├── accounts/               # Register, login, logout, user profile
│   ├── models.py           # UserProfile model + auto-create signal
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/
├── courses/                 # Course catalog + admin CRUD + search/filter
│   ├── models.py            # Course model
│   ├── management/commands/load_courses.py
│   └── templates/courses/
├── recommender/              # The ML recommendation engine
│   ├── ml_engine.py          # TF-IDF + Cosine Similarity core
│   ├── models.py             # SavedCourse, RecommendationHistory
│   ├── management/commands/train_model.py
│   └── templates/recommender/
├── smartcourse/               # Django project settings/urls
├── templates/                 # Shared templates (base.html, home.html)
├── static/css/                # Custom CSS
├── dataset/
│   ├── courses.csv            # 200-course dataset
│   └── generate_dataset.py    # Script that generated it
├── saved_model/                # Trained TF-IDF model (joblib files)
├── screenshots/                 # App screenshots for documentation
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation Guide

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd smart-course-recommender

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin account
python manage.py createsuperuser

# 6. Load the course dataset into the database
python manage.py load_courses

# 7. Train the ML recommendation model
python manage.py train_model

# 8. Run the development server
python manage.py runserver
```

Then visit **http://127.0.0.1:8000/**

> **Important:** Re-run `python manage.py train_model` any time you add,
> edit, or remove courses — the trained model is a static snapshot and
> won't reflect changes until retrained.

---

## Dataset Description

`dataset/courses.csv` contains **200 courses** across 10 career domains
(Web Development, Data Science, Machine Learning, Cloud Computing,
Cybersecurity, Mobile Development, UI/UX Design, Business & Management,
Blockchain, Game Development).

| Column | Description |
|---|---|
| course_name | Title of the course |
| platform | Coursera, Udemy, edX, Udacity, LinkedIn Learning, Pluralsight |
| category | Broad subject area |
| career_domain | Job role this course supports |
| skills_required | Comma-separated prerequisite/associated skills |
| tags | Comma-separated keywords used for ML matching |
| difficulty | Beginner / Intermediate / Advanced |
| duration | Course length |
| rating | Course rating (3.6–4.9) |
| description | Full text description |

---

## Algorithm Explanation

### Why TF-IDF?

TF-IDF (**Term Frequency–Inverse Document Frequency**) converts each
course's text (category, skills, tags, description) into a numeric
vector. It weights words by how *distinctive* they are: common filler
words ("course", "learn") are pushed down in importance, while rare,
meaningful words ("Kubernetes", "cryptography") are pushed up. This
means two courses sharing distinctive terms are considered more similar
than two that only share generic words.

### Why Cosine Similarity?

Once every course (and the user's profile) becomes a TF-IDF vector, we
need a way to measure closeness. **Cosine similarity** measures the angle
between two vectors rather than their length — so a short course
description and a long one about the same topic still score as similar,
since similarity is based on word *pattern*, not word *count*. Scores
range from 0 (unrelated) to 1 (identical topic focus).

### How the recommender works, step by step

1. Every course is converted into one text blob (category + career domain
   + skills + tags + difficulty + description).
2. TF-IDF is **fit** once across all 200 courses, producing a matrix
   where each row is a course.
3. This fitted vectorizer and matrix are saved to disk with **joblib**,
   so the web app never retrains on every request — it just loads the
   saved model (`saved_model/*.joblib`).
4. When a user submits the recommendation form, their profile
   (skills + interests + career goal + experience level) is converted
   into the *same kind* of text blob, and **transformed** (not re-fit)
   using the already-fitted vectorizer.
5. **Cosine similarity** is computed between the user's vector and every
   course vector.
6. Courses are sorted by similarity score, and the top 10 are returned
   with their scores.

### Advantages

- Works from day one — no "cold start" problem (unlike collaborative
  filtering, which needs many users' behavior data first).
- Explainable — you can point to which shared words drove a match.
- No dependency on tracking other users' ratings/clicks.

### Limitations

- Only as good as the text quality — vague descriptions produce vague
  matches.
- Can't surface novel interests outside what the user described
  (collaborative filtering can surprise users; content-based can't).
- No social proof signal (e.g. "94% of similar users loved this").

---

## Features

**User Module:** Register, Login, Logout, Profile (skills, interests,
career goal, experience level, weekly study hours, preferred platform).

**Recommendation Module:** Input form → top 10 ML-ranked courses with
name, platform, duration, difficulty, rating, and similarity score.

**Admin Module:** Full CRUD on courses via Django Admin, dataset loading
via management command, user management.

**Extras:** Search & filter the course catalog (by name, difficulty,
platform), save favorite courses, recommendation history, responsive
Bootstrap UI, form validation, friendly error handling.

---

## Future Enhancements

- 🤖 AI Chatbot for career guidance
- 📊 Skill Gap Analysis (compare current skills vs. target role)
- 🗺️ Learning Roadmap Generator
- 📄 Resume Analyzer
- 📈 Course Completion Prediction
- 💼 Job Recommendation integration
- 🏆 Certificate Tracker
- 🔄 Hybrid recommender (add collaborative filtering using other users'
  saved courses and ratings, on top of the existing content-based engine)

---

## Resume / LinkedIn / GitHub Content

### Resume Bullet Points

- Built a full-stack Smart Course Recommendation System using Django and
  Scikit-learn, implementing a content-based ML recommender (TF-IDF +
  Cosine Similarity) that matches user profiles against a 200-course
  catalog.
- Designed and implemented Django models, forms, views, and admin
  interfaces for user authentication, course management, and a
  recommendation history/favorites system.
- Engineered an ML pipeline that vectorizes course metadata with TF-IDF,
  persists the trained model via Joblib, and serves real-time similarity
  scored recommendations through Django views.
- Built a responsive Bootstrap 5 frontend with search, multi-field
  filtering, and personalized dashboards, backed by a SQLite database.

### GitHub Project Description

> A Django + Scikit-learn web app that recommends online courses using a
> content-based ML recommender (TF-IDF vectorization + cosine similarity).
> Users provide their skills, interests, and career goals, and get
> ranked, explainable course recommendations from a 200-course dataset.
> Includes full user auth, an admin panel, saved favorites, and
> recommendation history.

### LinkedIn Project Description

> 🚀 Built a Smart Course Recommendation System — a full-stack Django
> web app that uses a Machine Learning content-based recommender
> (TF-IDF + Cosine Similarity) to match users with the most relevant
> online courses based on their skills, interests, and career goals.
> Implemented end-to-end: Django backend, Scikit-learn ML pipeline,
> Bootstrap frontend, and a SQLite-backed admin panel for managing a
> 200-course catalog. #Django #MachineLearning #Python #WebDevelopment
