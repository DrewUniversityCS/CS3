from crispy_forms.layout import Layout, Submit
from django.forms import ModelForm, CheckboxSelectMultiple, Textarea
from crispy_forms.helper import FormHelper

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


def get_dynamic_model_form(dynamic_model):
    """
    Return a form class based on dynamic_model
    """

    class DynamicModelForm(CrispyModelForm):
        class Meta:
            model = dynamic_model
            fields = "__all__"
            widgets = widget_dict
            labels = label_dict

    return DynamicModelForm
