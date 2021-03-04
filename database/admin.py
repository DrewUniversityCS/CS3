from django.contrib import admin

from .models.relationships import CourseOverlapPreference, Registration, RoomPreference, TimePreference, \
    CoursePreference
from .models.schedule_models import Course, Section, Schedule, Weekdays, TimeBlock
from .models.structural_models import Department, Building, Room
from .models.user_models import Student, Teacher

models = [Department, Building, Room, Course, Section, Schedule, Weekdays, TimeBlock, Student, Teacher,
          CourseOverlapPreference, Registration, RoomPreference, TimePreference, CoursePreference]

for model in models:
    admin.site.register(model)
