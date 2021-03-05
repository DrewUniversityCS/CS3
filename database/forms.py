from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from database.models.structural_models import Department, Room, Building


class CrispyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyModelForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))


class DepartmentForm(CrispyModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class BuildingForm(CrispyModelForm):
    class Meta:
        model = Building
        fields = "__all__"


class RoomForm(CrispyModelForm):
    class Meta:
        model = Room
        fields = "__all__"
