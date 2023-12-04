from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('change_subjects/', views.change_subjects, name='change_subjects'),
    path('create_session/', views.create_session, name='create_session'),
    path('review/<int:session_id>/', views.review, name='review')
]