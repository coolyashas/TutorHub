from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=10, choices=[('math','Math'),('physics','Physics'),('english','English')])

    def __str__(self):
        return self.get_name_display() #to display "Math" instead of "Object 1" when the form is loaded into the page

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('student','Student'), ('tutor','Tutor')])
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.get_type_display()

class Session(models.Model):
    date_time = models.DateTimeField()
    tutor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sessions_as_tutor')
    subject = models.OneToOneField(Subject, on_delete=models.RESTRICT, default=None)
    status = models.CharField(max_length=20, choices=[('scheduled','Scheduled'), ('accepted','Accepted'), 
                                                      ('finished','Finished')], default='scheduled')

    def __str__(self):
        return self.get_status_display()

class Attendance(models.Model):
    session = models.OneToOneField(Session, on_delete=models.RESTRICT)
    student = models.OneToOneField(UserProfile, on_delete=models.RESTRICT)
    tutor_review = models.TextField()
    student_review = models.TextField()

    def __str__(self):
        return self.student.user