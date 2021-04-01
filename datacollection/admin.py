from django.contrib import admin

from datacollection.models import PreferenceForm, PreferenceFormEntry

models = [PreferenceForm, PreferenceFormEntry]

for model in models:
    admin.site.register(model)
