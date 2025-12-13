from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Company

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.USER_ROLES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'location', 'website', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://'}),
        }
