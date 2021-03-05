from django.shortcuts import render

from database.forms import DepartmentForm, RoomForm, BuildingForm, StudentForm, TeacherForm, CourseForm, SectionForm, \
    ScheduleForm, TimeblockForm, CoursePreferenceForm, OverlapPreference, OverlapPreferenceForm, RoomPreferenceForm, \
    TimeblockPreferenceForm, RegistrationForm
from database.models.relationships import CoursePreference, RoomPreference, TimeblockPreference, Registration
from database.models.schedule_models import Course, Section, Schedule, Timeblock
from database.models.structural_models import Department, Room, Building
from database.models.user_models import Student, Teacher

# User Model Views


def student_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Student.objects.all()
    form = StudentForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def teacher_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Teacher.objects.all()
    form = TeacherForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


# Structural Model Views


def department_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Department.objects.all()
    form = DepartmentForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def room_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Room.objects.all()
    form = RoomForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def building_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Building.objects.all()
    form = BuildingForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


# Schedule Model Views


def course_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Course.objects.all()
    form = CourseForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def section_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Section.objects.all()
    form = SectionForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def schedule_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Schedule.objects.all()
    form = ScheduleForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def timeblock_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Timeblock.objects.all()
    form = TimeblockForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


# Relationship Model Views


def course_preference_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = CoursePreference.objects.all()
    form = CoursePreferenceForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def overlap_preference_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = OverlapPreference.objects.all()
    form = OverlapPreferenceForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def room_preference_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = RoomPreference.objects.all()
    form = RoomPreferenceForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def timeblock_preference_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = TimeblockPreference.objects.all()
    form = TimeblockPreferenceForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})


def registration_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Registration.objects.all()
    form = RegistrationForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})