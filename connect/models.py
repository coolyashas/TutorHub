from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=10, choices=[('math', 'Math'), ('physics', 'Physics'), ('english', 'English')])

    def __str__(self):
        return self.get_name_display()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('student', 'Student'), ('tutor', 'Tutor')])
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username

class Session(models.Model):
    date_time = models.DateTimeField()
    tutor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sessions_as_tutor')
    #One tutor can have multiple session records
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT)
    #One subject can have multiple session records
    duration = models.DurationField(default=timedelta(hours=1))
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('booked', 'Booked'), 
                                                      ('finished', 'Finished'), ('missed', 'Missed')], 
                                                      default='scheduled')
    unique_link = models.CharField(max_length=100, default='meet.google.com')

    def __str__(self):
        return self.get_status_display()

class Attendance(models.Model):
    session = models.OneToOneField(Session, on_delete=models.RESTRICT)
    student = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    tutor_review = models.TextField(null=True) #by default
    student_review = models.TextField(null=True)
    tutor_rating = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1),MaxValueValidator(5)]
        )
    student_rating = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1),MaxValueValidator(5)]
        )

    def __str__(self):
        return str(self.student.user)