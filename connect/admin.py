from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Subject)
admin.site.register(UserProfile)
admin.site.register(Session)
admin.site.register(Attendance)