from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, CompanyForm

from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()  

    return render(request, 'company/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
        else:
            messages.error( request, 'invalid username or password')
    else:
        form = CustomLoginForm()

    return render(request, 'company/login.html', {'form': form})

def logout_view(request):
    logout(request)
    
    return redirect('feed')


def company_create(request):
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
                       
    else:
        form = CompanyForm()

    return render(request, 'company/company_form.html', {'form': form})




