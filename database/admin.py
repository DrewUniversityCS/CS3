from django.contrib import admin

from .models.structural_models import Department, Building, Room
from .models.schedule_models import Course, Section, Schedule, Weekday, TimeBlock
from .models.user_models import Student, Teacher
from .models.relationships import CourseOverlapPreference, SectionRegistration, CourseRoomPreference, \
    CourseTimeBlockPreference, StudentCoursePreference, TeacherCoursePreference, TeacherRoomPreference,\
    TeacherTimeBlockPreference

models = [Department, Building, Room, Course, Section, Schedule, Weekday, TimeBlock, Student, Teacher,
          CourseOverlapPreference, SectionRegistration, CourseRoomPreference, CourseTimeBlockPreference,
          StudentCoursePreference, TeacherCoursePreference, TeacherRoomPreference, TeacherTimeBlockPreference]

for model in models:
    admin.site.register(model)
