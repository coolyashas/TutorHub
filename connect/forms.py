from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.utils.translation import gettext_lazy as _
from .models import Session

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
    tutor_rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    student_review = forms.CharField(widget=forms.Textarea)
    student_rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    attended = forms.BooleanField()

    """def clean(self):
        cleaned_data = super().clean()
        attended = cleaned_data.get('attended', False)

        if attended and not cleaned_data.get('student_review'):
            self.add_error('student_review', 'student_review field is required.')
        if attended and not cleaned_data.get('student_rating'):
            self.add_error('student_rating', 'student_rating field is required.')

        return cleaned_data"""


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
        fields = ['date_time', 'subject', 'duration'] 
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'duration': forms.TextInput(attrs={'placeholder': _('hours:minutes:seconds')})
        }