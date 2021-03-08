import csv
import io

from django import forms


class DataForm(forms.Form):
    data_file = forms.FileField()

    def process_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        for line in reader:
            """
            get line
            get column values
            create db model with column values
            save db model
            repeat      
            """
            print(line)
