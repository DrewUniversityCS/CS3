from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import ModelForm, CheckboxSelectMultiple, Textarea, CharField, \
    EmailField

from accounts.models import BaseUser
from database.models.user_models import Teacher, Student

widget_dict = {
    "comments": Textarea(attrs={'rows': 5, 'cols': 20}),
    "registrations": CheckboxSelectMultiple()
}

label_dict = {
    "student_id": "Student ID Number",
    "class_standing": "Class Standing",
    "overseeing_department": "Overseeing Department",
    "approving_teacher": "Confirming Faculty Member",
    "approval": "Already Approved",
    "department_head": "Department Head",
    "max_occupancy": "Maximum Occupancy",
    "max_enrollment": "Maximum Enrollment",
    "overlap_preferences": "Overlap Preferences",
    "room_preferences": "Room Preferences",
    "time_preferences": "Time Preferences",
    "section_id": "Section ID Number",
    "primary_instructor": "Primary Instructor",
    "other_instructor": "Secondary Instructor / Assisting Faculty",
    "start_hour": "Starting Hour",
    "start_minutes": "Starting Minutes",
    "end_hour": "Ending Hour",
    "end_minutes": "Ending Minutes"
}


class CrispyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout()
        self.helper.layout.append(Submit('save', 'save'))

        super(CrispyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = widget_dict
        labels = label_dict


def make_user_form(dynamic_model):
    class UserForm(CrispyModelForm):
        first_name = CharField(max_length=256)
        last_name = CharField(max_length=256)
        email = EmailField()

        def save(self, **kwargs):
            cleaned_data = self.cleaned_data

            user_object = BaseUser(
                username=cleaned_data["email"].split("@")[0],
                email=cleaned_data["email"],
                password=BaseUser.objects.make_random_password(),
                first_name=cleaned_data["first_name"],
                last_name=cleaned_data["last_name"]
            )

            if dynamic_model == Student:
                student = Student(
                    student_id=cleaned_data["student_id"],
                    class_standing=cleaned_data["class_standing"],
                    user=user_object,
                    user_id=user_object.id
                )
                user_object.save()
                student.save()
            else:
                teacher = Teacher(
                    overseeing_department=cleaned_data["overseeing_department"],
                    user=user_object,
                    user_id=user_object.id
                )
                user_object.save()
                teacher.save()

        class Meta:
            model = dynamic_model
            exclude = ['user', 'registrations']
            field_order = [
                'first_name',
                'last_name',
                'email',
                'class_standing',
                'student_id',
                'registrations',
                'overseeing_department'
            ]

    return UserForm


def get_dynamic_model_form(dynamic_model):
    """
    Return a form class based on dynamic_model
    """

    if dynamic_model not in [Teacher, Student]:
        class DynamicModelForm(CrispyModelForm):
            class Meta:
                model = dynamic_model
                fields = "__all__"
    else:
        return make_user_form(dynamic_model)

    return DynamicModelForm
