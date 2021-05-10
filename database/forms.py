from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Exists, OuterRef
from django.forms import ModelForm, CheckboxSelectMultiple, CharField, \
    EmailField, ModelChoiceField, Form, ModelMultipleChoiceField, HiddenInput, Select, BooleanField, IntegerField, \
    ChoiceField

from accounts.models import BaseUser
from database.enums import YEAR_IN_SCHOOL_CHOICES
from database.models.schedule_models import Schedule, Course
from database.models.structural_models import ModelSet, SetMembership
from database.models.user_models import Teacher, Student
from database.validators import student_id_validator

tailwind_dropdown = Select(attrs={
    'class': 'bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none '
             'leading-normal text-gray-700'})

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
    "end_minutes": "Ending Minutes",
    "obj_type": "Object Type",
    "obj_1_type": "Member A Type"
}


class CrispyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout()
        self.helper.layout.append(Submit('save', 'save'))

        super(CrispyModelForm, self).__init__(*args, **kwargs)


def make_user_form(dynamic_model):
    class UserForm(CrispyModelForm):

        name_required = False
        if dynamic_model == Teacher:
            name_required = True

        first_name = CharField(max_length=256, required=name_required)
        last_name = CharField(max_length=256, required=name_required)
        if dynamic_model == Student:
            student_id = IntegerField(validators=[student_id_validator], required=False)
            class_standing = ChoiceField(choices=YEAR_IN_SCHOOL_CHOICES, required=False)
        email = EmailField()

        def clean(self):
            cleaned_data = super().clean()
            last_name = cleaned_data.get("last_name")
            first_name = cleaned_data.get("first_name")
            email = cleaned_data.get("email")
            if any(i.isdigit() for i in first_name):
                raise ValidationError("First Name must contain only characters.")
            elif any(i.isdigit() for i in last_name):
                raise ValidationError("Last Name must contain only characters.")
            if not self.instance.id:
                if BaseUser.objects.filter(username=email).exists():
                    raise ValidationError("Email is already registered. Please use a different email.")
                elif BaseUser.objects.filter(email=email).exists():
                    raise ValidationError("Email is already registered. Please use a different email.")
                elif BaseUser.objects.filter(username=email.split('@')[0]).exists():
                    raise ValidationError("Email is already registered. Please use a different email.")
            return cleaned_data

        def save(self, **kwargs):
            cleaned_data = self.cleaned_data
            """
            The instance ID exists only in an edit form, so this way we know we are updating and not creating an object
            """
            if self.instance.id is not None:
                if dynamic_model == Student:
                    student = Student.objects.filter(pk=self.instance.id)
                    user_object = BaseUser.objects.filter(pk=student[0].user_id)

                    user_object.update(
                        username=cleaned_data.get("email").split("@")[0],
                        email=cleaned_data.get("email"),
                        first_name=cleaned_data.get("first_name"),
                        last_name=cleaned_data.get("last_name")
                    )
                    student.update(
                        student_id=cleaned_data.get("student_id"),
                        class_standing=cleaned_data.get("class_standing"),
                    )
                elif dynamic_model == Teacher:
                    teacher = Teacher.objects.filter(pk=self.instance.id)
                    user_object = BaseUser.objects.filter(pk=teacher[0].user_id)
                    user_object.update(
                        username=cleaned_data.get("email").split("@")[0],
                        email=cleaned_data.get("email"),
                        first_name=cleaned_data.get("first_name"),
                        last_name=cleaned_data.get("last_name")
                    )
                    teacher.update(
                        department=cleaned_data.get("department")
                    )
            else:
                if dynamic_model == Student:
                    user_object = BaseUser(
                        username=cleaned_data.get("email").split("@")[0],
                        email=cleaned_data.get("email"),
                        password=BaseUser.objects.make_random_password(),
                        first_name=cleaned_data.get("first_name"),
                        last_name=cleaned_data.get("last_name")
                    )
                    student = Student(
                        student_id=cleaned_data.get("student_id"),
                        class_standing=cleaned_data.get("class_standing"),
                        user=user_object,
                        user_id=user_object.id
                    )
                    user_object.save()
                    student.save()
                else:
                    user_object = BaseUser(
                        username=cleaned_data.get("email").split("@")[0],
                        email=cleaned_data.get("email"),
                        password=BaseUser.objects.make_random_password(),
                        first_name=cleaned_data.get("first_name"),
                        last_name=cleaned_data.get("last_name")
                    )
                    teacher = Teacher(
                        user=user_object,
                        user_id=user_object.id,
                        department=cleaned_data.get("department")
                    )
                    user_object.save()
                    teacher.save()

        class Meta:
            model = dynamic_model
            exclude = ['user', 'registrations', 'student_id', 'first_name', 'last_name', 'class_standing']
            if dynamic_model == Teacher:
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
            labels = label_dict

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
                labels = label_dict
    else:
        return make_user_form(dynamic_model)

    return DynamicModelForm


def get_dynamic_model_choice_set_form(dynamic_model, crud_type):
    class DynamicModelSetForm(Form):
        set = ModelChoiceField(queryset=ModelSet.objects.all(), required=False)

        if crud_type == "create":
            new_set_name = CharField(max_length=256, required=False)

        choices = ModelMultipleChoiceField(
            queryset=dynamic_model.objects.all(),
            widget=CheckboxSelectMultiple(),
            label=f'{dynamic_model.__name__}s'
        )

        def clean(self):
            cleaned_data = super().clean()
            if crud_type == "create":
                chosen_set = cleaned_data.get("set")
                new_set = cleaned_data.get("new_set_name")
                if chosen_set is None and new_set == "":
                    raise ValidationError("Please specify either a new or existing set.")
                elif chosen_set is not None and new_set != "":
                    raise ValidationError("You cannot specify both an existing and new set at the same time.")
            return cleaned_data

        def __init__(self, *args, **kwargs):
            remove_set = kwargs.pop('remove_set', False)
            super(DynamicModelSetForm, self).__init__(*args, **kwargs)
            if remove_set:
                self.fields['set'].widget.attrs['style'] = 'pointer-events:none; background:#d3d3d3;'
                self.fields['set'].initial = kwargs['initial']['set'].id
            else:
                self.fields['set'].queryset = ModelSet.objects.filter(
                    ~Exists(SetMembership.objects.filter(set=OuterRef('pk'))),
                    obj_type__model=dynamic_model.__name__.lower()
                )

    return DynamicModelSetForm


class CreateBulkSectionsForm(Form):
    schedule = ModelChoiceField(queryset=Schedule.objects.all())
    courses = ModelMultipleChoiceField(queryset=ModelSet.objects.filter(obj_type__model='course'))


class EmptyForm(Form):
    placeholder_field = CharField(widget=HiddenInput(), required=False)


class CreatePreferenceForm(Form):
    preference_models = ['course', 'section', 'timeblock', 'baseuser']

    object_1_type = ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=preference_models), label="Member A Type",
        widget=tailwind_dropdown)
    object_1 = ModelChoiceField(queryset=Course.objects.none(), widget=tailwind_dropdown)
    object_2_type = ModelChoiceField(queryset=ContentType.objects.filter(model__in=preference_models),
                                     label="Member B Type",
                                     widget=tailwind_dropdown)
    object_2 = ModelChoiceField(queryset=Course.objects.none(),
                                widget=tailwind_dropdown)

    weight = BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['object_1'].queryset = Course.objects.all()
        self.fields['object_2'].queryset = Course.objects.all()

        if 'object_1_type' in self.data:
            try:
                object_1_type_id = int(self.data.get('object_1_type'))
                object_1_type = ContentType.objects.get_for_id(object_1_type_id)
                self.fields['object_1'].queryset = object_1_type.get_all_objects_for_this_type()
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset

        if 'object_2_type' in self.data:
            try:
                object_2_type_id = int(self.data.get('object_2_type'))
                object_2_type = ContentType.objects.get_for_id(object_2_type_id)
                self.fields['object_2'].queryset = object_2_type.get_all_objects_for_this_type()
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset

    def clean(self):
        cleaned_data = super().clean()

        obj_1_type, obj_2_type = cleaned_data['object_1_type'], cleaned_data['object_2_type']

        if obj_1_type == obj_2_type:
            if obj_1_type == ContentType.objects.get(app_label='database', model='timeblock'):
                raise ValidationError("You cannot create a preference between two timeblocks")
            elif obj_2_type == ContentType.objects.get(app_label='accounts', model='baseuser'):
                raise ValidationError("You cannot create a preference between two teachers")

        return cleaned_data
