from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('review/', views.review, name='review'),
    path('change_subjects/', views.change_subjects, name='change_subjects'),
    path('schedule_session/', views.schedule_session, name='schedule_session')
]