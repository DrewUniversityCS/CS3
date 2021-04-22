from io import StringIO

from django.core.exceptions import ValidationError
from django.forms import Form, ChoiceField, FileField
from django.utils.safestring import mark_safe

from dataingest.logistics import required_course_fields, required_student_fields, required_preference_fields


def validate_csv_columns(col_names, category):
    if category == 'course':
        for field in required_course_fields:
            if field not in col_names:
                return False
        return True

    elif category == 'student':
        for field in required_student_fields:
            if field not in col_names:
                return False
        return True

    elif category == 'preference':
        for field in required_preference_fields:
            if field not in col_names:
                return False
        return True

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
        req_fields_cases = {'course': required_course_fields,
                            'student': required_student_fields,
                            'preference': required_preference_fields}

        required_fields = req_fields_cases.get(category)

        if file:
            data_set = file.read().decode('UTF-8')
            r = StringIO(data_set)
            col_names = next(r)

            columns_are_valid = validate_csv_columns(col_names, category)

            i = 0
            wrong_cat_cols = []
            wrong_cat_cols_index = []
            for i in range(len(required_fields)):
                if required_fields[i] in col_names:
                    i = i + 1

                elif required_fields[i] not in col_names:
                    wrong_cat_cols.append(required_fields[i])
                    wrong_cat_cols_index.append(i + 1)
                    i = i + 1

            string_ints = [str(int) for int in wrong_cat_cols_index]
            str_of_ints = ",".join(string_ints)

            if not columns_are_valid:
                raise ValidationError(mark_safe("File doesn't have the necessary column names. You gave: " + col_names +
                                                "<br />To correct this, change column number(s) "
                                                + str_of_ints + " to "
                                                + "\'" + ",".join(wrong_cat_cols) + "\'" + " in your csv!"))

        return cleaned_data
