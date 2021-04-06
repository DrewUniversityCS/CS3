from io import StringIO

from django.core.exceptions import ValidationError
from django.forms import Form, ChoiceField, FileField


def validate_csv_columns(col_names, category):
    if category == 'course':
        required_course_fields = ['department', 'name', 'number']

        for field in required_course_fields:
            if field not in col_names:
                print(field)
                return False
        return True

    elif category == 'student':
        required_student_fields = ['student_id', 'class_standing', 'first_name', 'last_name', 'email']

        for field in required_student_fields:
            if field not in col_names:
                print(field)
                return False
        return True

    elif category == 'preference':
        required_preference_fields = ['object_1_content_type', 'object_1', 'object_2_content_type', 'object_2']

        for field in required_preference_fields:
            if field not in col_names:
                print(field)
                return False
        return True

    else:
        return False


class UploadCSVFileForm(Form):
    category = ChoiceField(choices=(
        ('course', "Courses"),
        ('student', "Students"),
        ('preference', "Preferences"),
    ), required=True)
    file = FileField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data['file']
        category = cleaned_data['category']
        if file:
            data_set = file.read().decode('UTF-8')
            r = StringIO(data_set)
            col_names = next(r)

            columns_are_valid = validate_csv_columns(col_names, category)

            if not columns_are_valid:
                raise ValidationError("File doesn't have the necessary fields")

        return cleaned_data
