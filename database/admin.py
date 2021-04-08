from django.contrib import admin

from .models.schedule_models import Course, Section, Schedule, WeekdaySet, Timeblock
from .models.structural_models import Department, ModelSet, SetMembership, Preference
from .models.user_models import Student, Teacher

models = [Department, Course, Section, Schedule, WeekdaySet, Timeblock, Student, Teacher,
          Preference, ModelSet, SetMembership]

for model in models:
    admin.site.register(model)
