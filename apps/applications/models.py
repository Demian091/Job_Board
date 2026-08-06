from django.db import models
from apps.accounts.models import User
from apps.jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='applications/resumes/', blank=True)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    expected_salary = models.PositiveIntegerField(null=True, blank=True)
    notice_period = models.CharField(max_length=50, blank=True)  # e.g., "2 weeks"
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)  # Internal notes for employer
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant.email} - {self.job.title}"