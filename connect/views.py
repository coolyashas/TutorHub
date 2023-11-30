from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from .models import *

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): #ensuring inputs are correct
            user = form.save() #saves user to auth_user db
            
            print("form is valid")
            user_profile = UserProfile.objects.create(
                user=user, #this might be the problem
                type=form.cleaned_data['type']
            )
            print("create done")
            user_profile.subjects.set(form.cleaned_data['subjects'])
            print("set done")
                
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.type == 'student':
        sessions = Session.objects.filter(subject__in=user_profile.subjects.all())
    elif user_profile.type == 'tutor':
        sessions = user_profile.sessions_as_tutor.all()
    return render(request, 'home.html', {'user_profile': user_profile, 'sessions': sessions})

@login_required
def review(request):
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        return redirect('home')
    return render(request, 'review.html', {'form': form})

@login_required
def change_subjects(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SubjectSelectionForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SubjectSelectionForm(instance=user_profile)
    return render(request, 'subs.html', {'form': form})

@login_required
def schedule_session(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.tutor = user_profile
            session.save()
            return redirect('home')
    else:
        form = SessionForm()
    return render(request, 'schedule_session.html', {'form': form})