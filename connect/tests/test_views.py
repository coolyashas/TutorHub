from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from connect.models import UserProfile, Subject
from connect.forms import *

class UserProfileListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 13 user profiles for pagination tests
        number_of_profiles = 13

        for profile_id in range(number_of_profiles):
            
            user = User.objects.create(username=f'user{profile_id}')
            subject = Subject.objects.create(name=f'subject{profile_id}')

            user_profile = UserProfile.objects.create(
                user=user,
                type='student',
            )
            user_profile.subjects.add(subject)

    def test_register_view_url_exists_at_desired_location(self):
        response = self.client.get('/connect/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get('/connect/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view_url_exists_at_desired_location(self):
        response = self.client.get('/connect/logout/')
        self.assertEqual(response.status_code, 302)  # 302 for redirect to login page after logout

    def test_home_view_url_exists_at_desired_location(self):
        response = self.client.get('/connect/home/')
        self.assertEqual(response.status_code, 302)  # Assuming redirection to login page if not authenticated

    def test_review_view_url_exists_at_desired_location(self):
        response = self.client.get('/connect/review/')
        self.assertEqual(response.status_code, 302)  # Assuming redirection to login page if not authenticated

    def test_register_view_validation_failed(self):
        data = {'username': 'testuser', 'password1': 'testpassword', 'password2': 'wrongpassword', 'type': 'student'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        # Add more assertions for the display after validation failed as needed

    def test_register_view_validation_succeeded(self):
        
        subject = Subject.objects.get(name='subject0') #one of the subject objects created above in the clas method

        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'type': 'student',
            'subjects': [subject.id],  # Include the subject ID in the list
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Assuming redirection to home page after successful registration
        # Add more assertions for the display after validation succeeded as needed


    def test_change_subjects_view_initial_display(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user, type='student') 
        #it is necessary to create the above for authentication, even though variable
        #is not used, django will fail this test is UserProfile has not been created
        self.client.force_login(user)

        # Make a GET request to the change_subjects view
        response = self.client.get(reverse('change_subjects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subs.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SubjectSelectionForm)
        # Add more assertions for the initial display as needed

    def test_change_subjects_view_validation_succeeded(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user, type='student')
        subject = Subject.objects.create(name='testsubject')
        data = {'subjects': [subject.id]}
        response = self.client.post(reverse('change_subjects'), data)
        self.assertEqual(response.status_code, 302)  # Assuming redirection to home page after successful subject change
        # Add more assertions for the display after validation succeeded as needed

    def test_schedule_session_view_initial_display(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user, type='tutor')
        subject = Subject.objects.get(name='subject0')
        user_profile.subjects.add(subject)

        self.client.force_login(user)

        response = self.client.get(reverse('schedule_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_session.html')
        # Add more assertions for the initial display as needed


    def test_schedule_session_view_validation_succeeded(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(user=user, type='tutor')
        subject = Subject.objects.create(name='testsubject')
        data = {'date_time': '2023-11-30T12:00:00Z', 'subject': subject.id}
        response = self.client.post(reverse('schedule_session'), data)
        self.assertEqual(response.status_code, 302)  # Assuming redirection to home page after successful session scheduling
        # Add more assertions for the display after validation succeeded as needed