from django.test import TestCase
from django.contrib.auth.models import User
from connect.models import Subject, UserProfile, Session, Attendance

class SubjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Subject.objects.create(name='math')

    def test_name_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('name').max_length
        self.assertEqual(max_length, 10)

    def test_object_name_is_name(self):
        subject = Subject.objects.get(id=1)
        self.assertEqual(str(subject), subject.get_name_display())

class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=user, type='student')

    def test_type_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'type')

    def test_type_max_length(self):
        profile = UserProfile.objects.get(id=1)
        max_length = profile._meta.get_field('type').max_length
        self.assertEqual(max_length, 10)

    def test_object_name_is_type(self):
        profile = UserProfile.objects.get(id=1)
        self.assertEqual(str(profile), profile.get_type_display())

class SessionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='tutoruser', password='tutorpassword')
        tutor_profile = UserProfile.objects.create(user=user, type='tutor')
        subject = Subject.objects.create(name='math')
        Session.objects.create(date_time='2023-11-30T12:00:00Z', tutor=tutor_profile, subject=subject, status='scheduled')

    def test_date_time_label(self):
        session = Session.objects.get(id=1)
        field_label = session._meta.get_field('date_time').verbose_name
        self.assertEqual(field_label, 'date time')

    def test_tutor_label(self):
        session = Session.objects.get(id=1)
        field_label = session._meta.get_field('tutor').verbose_name
        self.assertEqual(field_label, 'tutor')

class AttendanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        tutor_user = User.objects.create_user(username='tutoruser', password='tutorpassword')
        tutor_profile = UserProfile.objects.create(user=tutor_user, type='tutor')

        student_user = User.objects.create_user(username='studentuser', password='studentpassword')
        student_profile = UserProfile.objects.create(user=student_user, type='student')

        subject = Subject.objects.create(name='math')

        session = Session.objects.create(date_time='2023-11-30T12:00:00Z', tutor=tutor_profile, subject=subject, status='scheduled')

        attendance = Attendance.objects.create(session=session, student=student_profile, tutor_review='Good', student_review='Excellent')

    def test_session_label(self):
        attendance = Attendance.objects.get(id=1)
        field_label = attendance._meta.get_field('session').verbose_name
        self.assertEqual(field_label, 'session')

    def test_student_label(self):
        attendance = Attendance.objects.get(id=1)
        field_label = attendance._meta.get_field('student').verbose_name
        self.assertEqual(field_label, 'student')

    def test_tutor_review_label(self):
        attendance = Attendance.objects.get(id=1)
        field_label = attendance._meta.get_field('tutor_review').verbose_name
        self.assertEqual(field_label, 'tutor review')

    def test_student_review_label(self):
        attendance = Attendance.objects.get(id=1)
        field_label = attendance._meta.get_field('student_review').verbose_name
        self.assertEqual(field_label, 'student review')