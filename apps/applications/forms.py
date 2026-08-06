from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume', 'portfolio_url', 'linkedin_url', 'expected_salary', 'notice_period']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Why are you a good fit for this role?'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'expected_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'notice_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 weeks'}),
        }