from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


def index(responce):
    return render(responce, 'index.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        form = RegisterForm()
    return render(request, "sign_up.html", {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'login successfully')
                return redirect('/')
            else:
                messages.error(request, f'wrong username or password')
    else:
        form = LoginForm()
    return render(request, "log_in.html", {'form': form})

def log_out(request):
    logout(request)
    messages.success(request, f'log out sucessfully')
    return redirect('/')