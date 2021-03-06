from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from database.models.relationships import CoursePreference, RoomPreference, TimeblockPreference, Registration, \
    OverlapPreference
from database.models.schedule_models import Course, Section, Schedule, Timeblock
from database.models.structural_models import Department, Room, Building
from database.models.user_models import Student, Teacher


class CrispyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyModelForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))


def get_dynamic_model_form(dynamic_model):
    """
    Return a form class based on dynamic_model
    """
    class DynamicModelForm(CrispyModelForm):
        class Meta:
            model = dynamic_model
            fields = "__all__"
    return DynamicModelForm

# User Model Forms



# class StudentForm(CrispyModelForm):
#     class Meta:
#         model = Student
#         fields = "__all__"
#
#
# class TeacherForm(CrispyModelForm):
#     class Meta:
#         model = Teacher
#         fields = "__all__"
#
# # Structural Model Forms
#
#
# class DepartmentForm(CrispyModelForm):
#     class Meta:
#         model = Department
#         fields = "__all__"
#
#
# class BuildingForm(CrispyModelForm):
#     class Meta:
#         model = Building
#         fields = "__all__"
#
#
# class RoomForm(CrispyModelForm):
#     class Meta:
#         model = Room
#         fields = "__all__"
#
#
# # Schedule Model Forms
#
#
# class CourseForm(CrispyModelForm):
#     class Meta:
#         model = Course
#         fields = "__all__"
#
#
# class SectionForm(CrispyModelForm):
#     class Meta:
#         model = Section
#         fields = "__all__"
#
#
# class ScheduleForm(CrispyModelForm):
#     class Meta:
#         model = Schedule
#         fields = "__all__"
#
#
# class TimeblockForm(CrispyModelForm):
#     class Meta:
#         model = Timeblock
#         fields = "__all__"
#
#
# # Relationship Model Forms
#
#
# class CoursePreferenceForm(CrispyModelForm):
#     class Meta:
#         model = CoursePreference
#         fields = "__all__"
#
#
# class OverlapPreferenceForm(CrispyModelForm):
#     class Meta:
#         model = OverlapPreference
#         fields = "__all__"
#
#
# class RoomPreferenceForm(CrispyModelForm):
#     class Meta:
#         model = RoomPreference
#         fields = "__all__"
#
#
# class TimeblockPreferenceForm(CrispyModelForm):
#     class Meta:
#         model = TimeblockPreference
#         fields = "__all__"
#
#
# class RegistrationForm(CrispyModelForm):
#     class Meta:
#         model = Registration
#         fields = "__all__"
