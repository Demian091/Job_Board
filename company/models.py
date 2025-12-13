from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_ROLES = (
        ('employer', 'Employer'),
        ('jobseeker', 'Job Seeker'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES)
    avatar= models.ImageField(null=True, default="avatar.svg")


    def __str__(self):
        return f"{self.username} ({self.role})"

class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length= 200, null= True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
