from django.contrib import admin

from .models.structural_models import Department, Building, Room
from .models.schedule_models import Course, Section, Schedule, Weekday, TimeBlock
from .models.user_models import StudentUser, TeacherUser

models = [Department, Building, Room, Course, Section, Schedule, Weekday, TimeBlock, StudentUser, TeacherUser]

for model in models:
    admin.site.register(model)
