from django import forms
from .models import Job
from django.utils import timezone
from datetime import timedelta

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 'responsibilities',
            'benefits', 'job_type', 'experience_level', 'salary_min',
            'salary_max', 'salary_currency', 'location', 'is_remote',
            'expires_at'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'benefits': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default expiration to 30 days from now
        if not self.instance.pk:
            self.fields['expires_at'].initial = timezone.now() + timedelta(days=30)
    
    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        
        if salary_min and salary_max and salary_min > salary_max:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")
        
        return cleaned_data