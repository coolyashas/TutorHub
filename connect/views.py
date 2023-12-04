from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): #ensuring inputs are correct
            user = form.save() #saves user to auth_user table
            
            print("form is valid")
            user_profile = UserProfile.objects.create(
                user=user,
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
def home(request): #logic is interesting so go over it

    user_profile = UserProfile.objects.get(user=request.user)
    sessions = Session.objects.filter(
            subject__in=user_profile.subjects.all()
        )
    print("Sessions: ", sessions)
    dic = {}

    if request.method == 'POST':
        if 'book_session' in request.POST:
            session_id = request.POST.get('book_session')
            session = Session.objects.get(pk=session_id)

            att = Attendance.objects.create(
                session=session,
                student=user_profile
            )
            dic[session] = att
            session.status = 'booked'
            session.save()

    else:
        if user_profile.type == 'tutor':
            sessions = user_profile.sessions_as_tutor.all()
            return render(request, 'home.html', {'user_profile': user_profile, 'sessions': sessions, 'curr':timezone.localtime(timezone.now())})

        for sess in sessions:
            att = Attendance.objects.filter(session=sess).first() #this was causing a bug in {% if user_profile == att.student %} cuz i forgot to add .first() here
            if att:
                dic[sess] = att

    return render(request, 'home.html', {'user_profile': user_profile, 'sessions': sessions, 'dic':dic, 'curr':timezone.localtime(timezone.now())})

@login_required
def review(request, session_id):
    user_profile = UserProfile.objects.get(user=request.user)
    session = Session.objects.get(pk=session_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            att = Attendance.objects.get(session=session).first()

            if user_profile == session.student:
                att.tutor_review = form.cleaned_data['tutor_review']
                att.tutor_rating = form.cleaned_data['tutor_rating']
            elif user_profile == session.tutor:
                att.student_review = form.cleaned_data['student_review']
                att.student_rating = form.cleaned_data['student_rating']

            if request.POST.get('attended') == 'attended':
                if att.student_review and att.student_rating:
                    session.status = 'finished'
            else:
                session.status = 'missed'

            att.save()
            session.save()
            return redirect('home')
        
    else:
        form =  ReviewForm()

    print("session_id received: ",  session_id)
    return render(request, 'review.html', {'form': form, 'user_profile': user_profile, 'session_id':session_id})

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
def create_session(request):
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
    return render(request, 'create_session.html', {'form': form})