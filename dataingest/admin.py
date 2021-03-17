from django.contrib import admin

from .models import CSV

models = [CSV]

for model in models:
    admin.site.register(CSV)
