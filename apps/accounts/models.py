from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('jobseeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='jobseeker')
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Job seeker specific
    resume = models.FileField(upload_to='resumes/', blank=True)
    skills = models.TextField(blank=True, help_text="Comma separated skills")
    experience_years = models.PositiveIntegerField(default=0)
    
    # Employer specific
    company_name = models.CharField(max_length=200, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email