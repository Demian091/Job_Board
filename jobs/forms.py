from django import forms
from .models import Job, Application, Post, Comment

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'category', 'salary']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
        
            "qualifications",
            "university",
            "gpa",
            "past_work_references",
            "cover_letter",
            "project_link"
        ]
        widgets = {
            "cover_letter": forms.Textarea(attrs={"rows": 4}),
            "qualifications": forms.Textarea(attrs={"rows": 3}),
            "past_work_references": forms.Textarea(attrs={"rows": 3}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What’s on your mind?',
                'rows': 3
            }),
        }




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment...'
            }),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment...'
            }),
        }