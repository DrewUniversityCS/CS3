from django import forms

from .models import CSV


class CSVForm(forms.ModelForm):
    class Meta:
        model = CSV
        fields = ('CSV_File_Name', 'CSV_File')
