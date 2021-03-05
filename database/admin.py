from django.contrib import admin
from .models.relationships import OverlapPreference, Registration, RoomPreference, TimeblockPreference, \
    CoursePreference
from .models.schedule_models import Course, Section, Schedule, WeekdaySet, Timeblock
from .models.structural_models import Department, Building, Room
from .models.user_models import Student, Teacher

models = [Department, Building, Room, Course, Section, Schedule, WeekdaySet, Timeblock, Student, Teacher,
          OverlapPreference, Registration, RoomPreference, TimeblockPreference, CoursePreference]

for model in models:
    admin.site.register(model)

