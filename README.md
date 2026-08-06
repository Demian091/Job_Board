# JobBoard - Django Job Portal

A full-featured job board web application built with Django. Employers can post jobs and manage applications, while job seekers can search and apply for positions.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)

## Features

### For Job Seekers
- Create profile with resume upload
- Search and filter jobs by keyword, location, type, experience level
- Apply to jobs with cover letter
- Track application status (Pending, Reviewing, Shortlisted, Rejected, Hired)
- Receive email notifications on status updates

### For Employers
- Company profile management
- Post job listings with detailed requirements
- View and manage applications
- Update application status with one click
- Email notifications sent to applicants automatically

### General Features
- Responsive Bootstrap 5 design
- User authentication (email-based)
- Role-based access (Job Seeker vs Employer)
- Featured job listings
- Company verification badges

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Database**: SQLite (development) / PostgreSQL (production)
- **Forms**: Django Crispy Forms
- **Deployment**: WhiteNoise (static files), Gunicorn

## Installation

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jobboard.git
   cd jobboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create `.env` file in project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

9. **demo data**
   ```bash
   python manage.py populate_data
   ```

## Project Structure

```
jobboard/
├── apps/
│   ├── accounts/          # Custom user model, authentication
│   ├── jobs/              # Job listings, search, CRUD
│   ├── companies/         # Company profiles
│   └── applications/      # Job applications, status management
├── config/                # Django settings, URLs, WSGI
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploads (resumes, logos)
├── manage.py
└── requirements.txt
```

## Usage Guide

### As Job Seeker
1. Sign up as "Job Seeker"
2. Complete profile (add resume, skills, experience)
3. Browse jobs at `/jobs/`
4. Click "Apply" on job details page
5. Track applications at `/applications/my-applications/`

### As Employer
1. Sign up as "Employer"
2. Create company profile at `/companies/create/`
3. Post jobs at `/jobs/create/`
4. View applications:
   - All applications: `/applications/manage/`
   - Per job: Go to "My Job Listings" → click applicant count
5. Update status via dropdown or detail page buttons

## Deployment

### Railway (Recommended)
1. Push code to GitHub
2. Connect Railway to repo
3. Add environment variables in Railway dashboard
4. Deploy automatically

### Manual (VPS/DigitalOcean)
```bash
# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn config.wsgi:application
```

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgres://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## API Endpoints

| URL | Description |
|-----|-------------|
| `/` | Home - Job listings |
| `/jobs/` | All jobs with search/filter |
| `/jobs/create/` | Post new job (employer only) |
| `/jobs/<slug>/` | Job detail |
| `/companies/` | Company directory |
| `/accounts/profile/` | User profile |
| `/applications/manage/` | Manage applications (employer) |
| `/applications/my-applications/` | My applications (job seeker) |

## Customization

### Adding New Job Types
Edit `apps/jobs/models.py`:
```python
JOB_TYPES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    # Add your type here
)
```

### Changing Email Templates
Modify `send_status_email` method in `apps/applications/views.py`

### Styling
Edit CSS variables in `templates/base.html`:
```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'apps'` | Add `sys.path.insert(0, str(BASE_DIR / 'apps'))` to settings.py |
| `NoReverseMatch: 'register'` | Change `{% url 'register' %}` to `{% url 'signup_jobseeker' %}` |
| Static files not loading | Run `python manage.py collectstatic` |
| Media files 404 in development | Add to `urls.py`: `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` |

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use GitHub Issues.

---

Built with ❤️ using Django