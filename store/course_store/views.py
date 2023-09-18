import datetime
from .forms import RegisterForm, LoginForm
from .models import Courses, Curchased_courses
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


def index(request):
    courses = Courses.objects.all()
    date = datetime.datetime.now().date()
    if request.user.is_authenticated:
        purchased_courses = Curchased_courses.objects.filter(user_id=request.user.id).all()
        purchased_courses_id = [i.course_id for i in purchased_courses]
        return render(request, 'index.html', {'courses': courses, 'date': date, 'list_id': purchased_courses_id})
    else:
        return render(request, 'index.html', {'courses': courses, 'date': date})


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
    messages.success(request, f'log out successfully')
    return redirect('/')


def buy_course(request):
    course_id = request.POST['buy']
    purchased_course = Curchased_courses.objects.create(user_id=request.user.id, course_id=course_id)
    return redirect('/')


def profile(request):
    courses_id = Curchased_courses.objects.filter(user_id=request.user.id).all()
    purchased_courses = [Courses.objects.filter(id=course_id.course_id).first() for course_id in courses_id]
    return render(request, 'profile.html', {'purchased_courses': purchased_courses})
