from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistrationForm(UserCreationForm):
    type = forms.ChoiceField(choices=[('student', 'Student'), ('tutor', 'Tutor')])
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReviewForm(forms.Form):
    tutor_review = forms.CharField(widget=forms.Textarea)
    student_review = forms.CharField(widget=forms.Textarea)

class SubjectSelectionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,
        }


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date_time', 'subject']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }