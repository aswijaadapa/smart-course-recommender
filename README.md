# 🎓 Smart Course Recommendation System

A full-stack web application that recommends personalized online courses
using a **content-based Machine Learning recommender** (TF-IDF + Cosine
Similarity), built with **Django** and **Scikit-learn**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Folder Structure](#folder-structure)
4. [Features](#features)


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

👤 Author Built by Aswija Devi Adapa Hemasri Cheparthi Jaya Hasini Kothapalli as a portfolio project. GitHub: @aswijaadapa @hemasricheparthi @KJH666-star
---

