from django.forms import Form, ChoiceField, FileField


class UploadCSVFileForm(Form):
    category = ChoiceField(choices=(
        ('course', "Courses"),
        ('student', "Students"),
        ('preference', "Preferences"),
    ))
    file = FileField()
