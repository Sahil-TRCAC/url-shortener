# 🚀 ShortLink Pro — URL Shortener with Analytics & OAuth

A production-ready **URL Shortener Web Application** built with Django, featuring secure authentication, Google OAuth login, and real-time analytics.

This project demonstrates real-world backend development including **authentication flows, database management, API design, and cloud deployment on Render.**

---

## 🌐 Live Demo

👉 https://url-shortener-django-stad.onrender.com

---

## ⚙️ Tech Stack

### Backend
- Django (Python)
- Django REST Framework
- Social Auth (Google OAuth2)
- Django ORM

### Database
- PostgreSQL (Production)
- SQLite (Local Development)

### Authentication
- Google OAuth 2.0
- Django Session-based Auth

### Deployment & Infra
- Render (Cloud Hosting)
- Gunicorn (WSGI Server)
- WhiteNoise (Static File Handling)

---

## 🔐 Features

### 🔑 Authentication
- Login with Google (OAuth 2.0)
- Manual login & registration
- Secure session management

---

### 🔗 URL Shortening
- Generate short links instantly
- Redirect to original URLs
- Unique short code generation

---

### 📊 Analytics Dashboard
- Track total URLs created
- Monitor click counts
- View user-specific data

---

### 🧱 Backend Architecture
- Modular Django project structure
- Clean separation of views, models, and routes
- Scalable and maintainable codebase

---

## 📡 API Endpoints

### Auth
- `GET /login/`
- `POST /register/`
- `GET /logout/`

### Core
- `POST /api/create/` → Create short URL  
- `GET /api/dashboard/` → Dashboard analytics  
- `GET /<short_code>/` → Redirect  

---

## 🧪 Example Workflow

1. Register / Login  
2. Create a short URL  
3. Share the link  
4. Track clicks via dashboard  

---

## ⚠️ Challenges Faced (Real-World Debugging)

- ❌ Google OAuth failing due to missing redirect URI  
- ❌ Session issues in production (cookies not persisting)  
- ❌ Database errors (`auth_user` table missing) due to migrations not run  
- ❌ Dependency conflicts during deployment  

### ✅ Solutions
- Configured OAuth redirect + origins correctly  
- Fixed session handling using secure cookies & proxy headers  
- Automated migrations in Render build process  
- Cleaned and optimized dependencies  

---

## ☁️ Deployment

Deployed on **Render** with:

- PostgreSQL database  
- Automated migrations (`manage.py migrate`)  
- Static file handling via WhiteNoise  
- Environment variable-based configuration  

---

## 📁 Project Structure
url-shortener-analytics/
├── core/ # Main app (views, models, logic)
├── shortener/ # Project settings
├── templates/ # HTML templates
├── static/ # Static files
├── manage.py
├── requirements.txt
└── .env


---

## ⚙️ Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/url-shortener-analytics.git
cd url-shortener-analytics

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver


