# RGSS Backend (Django REST Framework + PostgreSQL)

This backend provides APIs for:
- Registrations (role-wise user registrations)
- Donations
- Contact leads
- Blog posts
- Objectives
- Site settings
- Dashboard summary stats

## 1) Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set your PostgreSQL credentials.

## 2) PostgreSQL

Create database:

```sql
CREATE DATABASE rgss_db;
```

## 3) Run migrations and create admin user

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Optional demo data (blogs, objectives, settings, sample donation/contact):

```bash
python manage.py seed_rgss_demo
```

## 4) Run server

```bash
python manage.py runserver
```

- Django Admin: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`
- Token auth endpoint: `http://127.0.0.1:8000/api/auth/token/` (used by the Next.js `/admin` panel)

Sign in on `/admin` with the same username and password as your Django superuser.

## Main API Endpoints

- `GET/POST /api/registrations/`
- `GET/POST /api/donations/`
- `GET/POST /api/contacts/`
- `GET/POST /api/blogs/`
- `GET/POST /api/objectives/`
- `GET/POST /api/settings/`
- `GET /api/dashboard/summary/`
