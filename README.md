# Job Board Application

A Django-based job board platform where companies can post jobs and users can browse and apply.

## 🚀 Features
- User authentication (JWT)
- Company accounts
- Job posting and listing
- REST API support
- PostgreSQL database
- Static file handling with Whitenoise

## 🛠 Tech Stack
- Python 3.12
- Django 5.1
- Django REST Framework
- PostgreSQL
- Gunicorn
- Whitenoise

## ⚙️ Installation (Local)

```bash
git clone https://github.com/Demian091/Job_Board.git
cd jobBoard
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
