from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.accounts.models import User

class Company(models.Model):
    SIZE_CHOICES = (
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    cover_image = models.ImageField(upload_to='company_covers/', blank=True)
    description = models.TextField()
    website = models.URLField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    industry = models.CharField(max_length=100)
    company_size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    
    location = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'slug': self.slug})