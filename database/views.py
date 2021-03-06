from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView
from database.forms import get_dynamic_model_form
from database.models.relationships import CoursePreference, RoomPreference, TimeblockPreference, Registration, \
    OverlapPreference
from database.models.schedule_models import Course, Section, Schedule, Timeblock
from database.models.structural_models import Department, Room, Building
from database.models.user_models import Student, Teacher
from django.views.generic.edit import FormView, DeleteView

# from database.forms import DepartmentForm, RoomForm, BuildingForm, StudentForm, TeacherForm, CourseForm, SectionForm, \
#     ScheduleForm, TimeblockForm, CoursePreferenceForm, OverlapPreference, OverlapPreferenceForm, RoomPreferenceForm, \
#     TimeblockPreferenceForm, RegistrationForm
# from database.models.relationships import CoursePreference, RoomPreference, TimeblockPreference, Registration
# from database.models.schedule_models import Course, Section, Schedule, Timeblock
# from database.models.structural_models import Department, Room, Building
# from database.models.user_models import Student, Teacher

# User Model Views
class DynamicModelMixin(object):
    dynamic_model = None
    dynamic_model_name = None
    model_map_dict = {
        'students': Student,
        'teachers': Teacher,
        'registrations': Registration,
        'course-preferences': CoursePreference,
        'overlap-preferences': OverlapPreference,
        'room-preferences': RoomPreference,
        'timeblock-preferences': TimeblockPreference,
        'departments': Department,
        'buildings': Building,
        'rooms': Room,
        'schedules': Schedule,
        'courses': Course,
        'sections': Section,
        'timeblocks': Timeblock,
    }
    def dispatch(self, request, *args, **kwargs):
        self.dynamic_model_name = kwargs.get('model')
        dynamic_model = self.model_map_dict.get(self.dynamic_model_name , None)
        if dynamic_model:
            self.dynamic_model = dynamic_model
            return super().dispatch(request, args, kwargs)
        raise Http404
class CrudDeleteView(DynamicModelMixin, DeleteView):
    template_name = "crud/generic_delete_view.html"
    def get_object(self):
        return get_object_or_404(self.dynamic_model, pk=self.kwargs.get('id'))
    def get_success_url(self):
        return reverse('database:crud_model', kwargs={'model': self.dynamic_model_name})
class CrudView(DynamicModelMixin, FormView):
    template_name = "crud/generic_crud_view.html"
    context_object_name = 'all_objects'
    def get_form_class(self):
        return get_dynamic_model_form(self.dynamic_model)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'all_objects': self.dynamic_model.objects.all(),
            'dynamic_model_name': self.dynamic_model_name
        })
        return context
    def get_success_url(self):
        return self.request.path
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# def student_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Student.objects.all()
#     form = StudentForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def teacher_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Teacher.objects.all()
#     form = TeacherForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# # Structural Model Views
#
#
# def department_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Department.objects.all()
#     form = DepartmentForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def room_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Room.objects.all()
#     form = RoomForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def building_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Building.objects.all()
#     form = BuildingForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# # Schedule Model Views
#
#
# def course_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Course.objects.all()
#     form = CourseForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def section_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Section.objects.all()
#     form = SectionForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def schedule_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Schedule.objects.all()
#     form = ScheduleForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def timeblock_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Timeblock.objects.all()
#     form = TimeblockForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# # Relationship Model Views
#
#
# def course_preference_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = CoursePreference.objects.all()
#     form = CoursePreferenceForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def overlap_preference_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = OverlapPreference.objects.all()
#     form = OverlapPreferenceForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def room_preference_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = RoomPreference.objects.all()
#     form = RoomPreferenceForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def timeblock_preference_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = TimeblockPreference.objects.all()
#     form = TimeblockPreferenceForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})
#
#
# def registration_crud(request):
#     template_name = "crud/generic_crud_view.html"
#     all_objects = Registration.objects.all()
#     form = RegistrationForm()
#     return render(request, template_name, {"all_objects": all_objects, "form": form})