from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class JobSeekerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'jobseeker'
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
        return user

class EmployerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    company_name = forms.CharField(max_length=200, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'company_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employer'
        user.username = self.cleaned_data['email']
        user.company_name = self.cleaned_data['company_name']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'location', 'profile_picture', 'bio']
        
        # Job seeker fields
        if 'resume' in model._meta.get_fields():
            fields.extend(['resume', 'skills', 'experience_years'])