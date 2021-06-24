from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from .forms import *

def registration_view(request):
    context= {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # account = authenticate(username=username, password=raw_password)
            # login(request, account)
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    context = {}
    
    user = request.user
    if user.is_authenticated:
        return redirect('index')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return redirect('index')
    
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'account/login.html', context)
        
def account_vieu(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = 'Updated'
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username
            }
        )
    context['account_form'] = form
    
    
    
    return render(request, 'account/account.html', context)

def index(request):
    return render(request, 'index.html')