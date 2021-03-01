from django.contrib import admin

from .models.structural_models import Department, Building, Room
from .models.schedule_models import Course, Section, Schedule, Weekday, TimeBlock
from .models.user_models import Student, Teacher
from .models.relationships import CourseOverlapPreference, Registration, RoomPreference, TimePreference, \
    CoursePreference

models = [Department, Building, Room, Course, Section, Schedule, Weekday, TimeBlock, Student, Teacher,
          CourseOverlapPreference, Registration, RoomPreference, TimePreference, CoursePreference]

for model in models:
    admin.site.register(model)
