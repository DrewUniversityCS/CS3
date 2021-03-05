from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from database.models.user_models import Student


class CrispyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyModelForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))


class StudentForm(CrispyModelForm):
    class Meta:
        model = Student
        fields = [
            'user',
            'student_id',
            'class_standing'
        ]
