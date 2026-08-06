from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'logo', 'cover_image', 'description', 'website',
            'email', 'phone', 'industry', 'company_size', 'founded_year',
            'location', 'address', 'linkedin', 'twitter', 'facebook'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }