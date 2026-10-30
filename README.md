# Online Course Application with Django (tfjzl-final-cloud-app-with-database)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x%2F6.x-092e20.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.5.2-purple.svg)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enhanced Django-based Online Course learning platform developed as the **Final Project: Add New Assessment Features to an Online Course Application** within the **IBM Cloud Application Development / Full Stack Developer Certificate** on Coursera.

---

## 🌟 Key Features & Implementations

### 1. Data Models (`onlinecourse/models.py`)
- **Question Model**: One-to-many relationship with `Course` (and `Lesson`), stores question prompt, point value (`grade`), and includes `is_get_score(selected_ids)` method to evaluate correct learner answers.
- **Choice Model**: Connects to `Question`, holds choice option content and boolean flag `is_correct`.
- **Submission Model**: Connects `Enrollment` to multiple selected `Choice` items.

### 2. Django Admin Interface (`onlinecourse/admin.py`)
- Imports 7 model classes: `Course, Lesson, Instructor, Learner, Question, Choice, Submission`.
- **ChoiceInline**: Stacked/Tabular inline for choices embedded directly in `QuestionAdmin`.
- **QuestionInline**: Stacked/Tabular inline for questions embedded in `LessonAdmin` and `CourseAdmin`.
- **QuestionAdmin** & **LessonAdmin**: Full search, filtering, and inline management capabilities.

### 3. Responsive Course Details Template (`onlinecourse/templates/onlinecourse/course_details_bootstrap.html`)
- Displays course heading, descriptions, and collapsible lessons using Bootstrap cards and accordion.
- Integrates course final exam form with interactive checkboxes for all questions and choices.

### 4. Exam Views & URL Routing (`onlinecourse/views.py`, `onlinecourse/urls.py`)
- `submit(request, course_id)`: Extracts learner choices, creates a `Submission` record linked to user's enrollment, and redirects to results.
- `show_exam_result(request, course_id, submission_id)`: Calculates exam percentage against a 70% passing threshold and renders detailed question breakdown in `exam_result_bootstrap.html`.

---

## 📁 Repository Structure

```text
tfjzl-final-cloud-app-with-database/
├── README.md                                                          # Project documentation
├── manage.py                                                          # Django management CLI
├── myproject/                                                         # Django root configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── onlinecourse/                                                      # Main application module
│   ├── models.py                                                      # Task 1: Question, Choice, Submission models
│   ├── admin.py                                                       # Task 2: 7 imports, Inlines, QuestionAdmin, LessonAdmin
│   ├── views.py                                                       # Task 5: submit and show_exam_result views
│   ├── urls.py                                                        # Task 6: routes for submit and show_exam_result
│   └── templates/onlinecourse/
│       ├── course_details_bootstrap.html                              # Task 4: Course details & exam form
│       └── exam_result_bootstrap.html                                 # Exam evaluation template
├── 03-admin-site.png                                                  # Task 3: Django Admin verification screenshot
├── 07-final.png                                                       # Task 7: Exam result verification screenshot
└── LICENSE                                                            # MIT License
```

---

## 🚀 Setup & Local Execution

1. Clone repository:
   ```bash
   git clone https://github.com/SyukurGit/tfjzl-final-cloud-app-with-database.git
   cd tfjzl-final-cloud-app-with-database
   ```

2. Install dependencies:
   ```bash
   pip install django
   ```

3. Run migrations and start server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver 8000
   ```
   Open `http://localhost:8000/` in your browser.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
