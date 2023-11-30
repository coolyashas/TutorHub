from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from connect.models import Subject, UserProfile, Session
from connect.forms import RegistrationForm, LoginForm, ReviewForm, SubjectSelectionForm, SessionForm

class RegistrationFormTest(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name='math')

    def test_registration_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'type': 'student',
            'subjects': [self.subject.id],
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

class LoginFormTest(TestCase):

    def test_login_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

class ReviewFormTest(TestCase):

    def test_review_form(self):
        form_data = {
            'tutor_review': 'Good',
            'student_review': 'Excellent',
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

class SubjectSelectionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, type='student')
        self.subject = Subject.objects.create(name='math')

    def test_subject_selection_form(self):
        form_data = {
            'subjects': [self.subject.id],
        }
        form = SubjectSelectionForm(data=form_data, instance=self.user_profile)
        self.assertTrue(form.is_valid())

class SessionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tutoruser', password='tutorpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, type='tutor')
        self.subject = Subject.objects.create(name='math')

    def test_session_form(self):
        form_data = {
            'date_time': timezone.now(),
            'subject': self.subject.id,
        }
        form = SessionForm(data=form_data)
        self.assertTrue(form.is_valid())