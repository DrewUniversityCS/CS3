import io
from django import forms

from django.contrib.auth.models import User

import csv

class DataForm(forms.Form):
    data_file = forms.FileField()

    def process_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        for user in reader:
            User.objects.create_user(user['username'], email=user['email'])