from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'location', 'created_at')
    list_filter = ('category', 'location', 'company')
    search_fields = ('title', 'company__name')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'university', 'gpa', 'status', 'applied_at')
    list_filter = ('status', 'job__category', 'university')
    search_fields = ('job__title', 'applicant__username', 'university')
