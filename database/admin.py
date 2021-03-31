from django.contrib import admin

from .models.relationships import Preference
from .models.schedule_models import Course, Section, Schedule, WeekdaySet, Timeblock
from .models.structural_models import Department, ModelSet, SetMembership, PreferenceForm, \
    PreferenceFormEntry
from .models.user_models import Student, Teacher

models = [Department, Course, Section, Schedule, WeekdaySet, Timeblock, Student, Teacher,
          Preference, ModelSet, SetMembership, PreferenceForm, PreferenceFormEntry]

for model in models:
    admin.site.register(model)
