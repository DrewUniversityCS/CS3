from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize, deserialize
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView

from accounts.models import BaseUser
from database.forms import EmptyForm
from database.models.schedule_models import Course, Timeblock, Section
from database.models.structural_models import SetMembership, ModelSet
from database.views import DynamicModelMixin
from dataingest.forms import UploadCSVFileForm
from dataingest.logistics import create_courses, create_students, create_preferences, write_to_csv


class UploadCSVFileView(LoginRequiredMixin, FormView):
    template_name = 'dataingest/upload_csv_file.html'
    form_class = UploadCSVFileForm
    success_url = '/dataingest/upload/success'

    def form_valid(self, form):
        category = form.data['category']
        file = self.request.FILES['file']
        objects = []
        if category == 'course':
            objects = create_courses(file)
        elif category == 'student':
            users, objects = create_students(file)  # objects is students
            self.request.session['users'] = serialize('json', users)
        elif category == 'preference':
            objects = create_preferences(file)

        self.request.session['objects'] = serialize('json', objects)

        return HttpResponseRedirect(self.get_success_url())


class UploadCSVFileSuccessView(LoginRequiredMixin, FormView):
    template_name = "dataingest/upload_verification.html"
    form_class = EmptyForm
    success_url = "/dataingest/upload/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        objects = []
        # if there are user objects to handle
        users = self.request.session.get('users')
        if users is not None:
            self.request.session['users'] = None
            for obj in deserialize("json", users):
                obj.object.save()  # we are forced to temporarily save the user objects
                """
                I'm not yet sure how to deal with the situation where
                the user leaves the confirmation page without interacting with the form, so I am putting down a flag
                to signify that there are "rogue users" in the database - my thought is, this could be checked somewhere
                and these users purged if needed.
                """
                self.request.session['rogue_users_flag'] = True
        for obj in deserialize("json", self.request.session.get('objects')):
            objects.append(obj.object)

        context['objects'] = serialize("python", objects, use_natural_foreign_keys=True)

        return context

    def form_valid(self, form):
        if 'confirm' in self.request.POST:
            for obj in deserialize("json", self.request.session.get('objects')):
                obj.object.save()
        else:
            for obj in deserialize("json", self.request.session.get('objects')):
                try:
                    uid = obj.object.user.id
                    BaseUser.objects.filter(id=uid).delete()
                except AttributeError:
                    pass
        return redirect(self.success_url)


class DownloadCSVFileView(LoginRequiredMixin, DynamicModelMixin, FormView):
    template_name = "dataingest/download_csv_file.html"
    form_class = EmptyForm
    success_url = "/dataingest/download_csv"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data_(*args, **kwargs)
        return self.render_to_response(context)

    def get_context_data_(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        set_id = args[1]['id']
        objects = SetMembership.objects.filter(set__id=set_id,
                                               content_type__model=self.dynamic_model.__name__.lower())
        objs = []
        for obj in objects:
            objs.append(obj.member_object)

        serialized_objs = serialize("python", objs, use_natural_foreign_keys=True)

        context['field_data'] = serialized_objs
        context['object'] = f"{ModelSet.objects.get(id=set_id)} - {self.dynamic_model.__name__}s"

        self.request.session['objects'] = serialized_objs
        return context


def download_as_csv(request):
    deserialized_objs = request.session['objects']
    cols = list(deserialized_objs[0]['fields'].keys())
    filename = 'courses_export.csv'

    if 'user' in cols:  # student upload
        cols.remove('user')
        cols.append('first_name')
        cols.append('last_name')
        cols.append('email')
        filename = 'students_export.csv'

    if 'object_1_id' in cols:  # preference upload
        cols.remove('object_1_id')
        cols.remove('object_2_id')
        cols.append('object_1_natural_id')
        cols.append('object_2_natural_id')
        filename = 'preferences_export.csv'

    rows = []
    for obj in deserialized_objs:
        dict = obj['fields']
        if 'user' in dict:
            user_data = list(dict['user'].values())
            row_data = [dict['student_id'], dict['class_standing']]
            row_data.extend(user_data)
            rows.append(row_data)
        elif 'object_1_id' in dict:
            object_1_natural_id = ''
            if dict['object_1_content_type'] == ['database', 'course']:
                object_1_natural_id = Course.objects.get(id=dict['object_1_id']).name
                dict['object_1_content_type'] = 'course'
            elif dict['object_1_content_type'] == ['accounts', 'baseuser']:
                object_1_natural_id = BaseUser.objects.get(id=dict['object_1_id']).email
                dict['object_1_content_type'] = 'teacher'
            elif dict['object_1_content_type'] == ['database', 'timeblock']:
                object_1_natural_id = Timeblock.objects.get(id=dict['object_1_id']).block_id
                dict['object_1_content_type'] = 'timeblock'
            elif dict['object_1_content_type'] == ['database', 'section']:
                object_1_natural_id = Section.objects.get(id=dict['object_1_id']).section_id
                dict['object_1_content_type'] = 'section'

            object_2_natural_id = ''
            if dict['object_2_content_type'] == ['database', 'course']:
                object_2_natural_id = Course.objects.get(id=dict['object_2_id']).name
                dict['object_2_content_type'] = 'course'
            elif dict['object_2_content_type'] == ['accounts', 'baseuser']:
                object_2_natural_id = BaseUser.objects.get(id=dict['object_2_id']).email
                dict['object_2_content_type'] = 'teacher'
            elif dict['object_2_content_type'] == ['database', 'timeblock']:
                object_2_natural_id = Timeblock.objects.get(id=dict['object_2_id']).block_id
                dict['object_2_content_type'] = 'timeblock'
            elif dict['object_2_content_type'] == ['database', 'section']:
                object_2_natural_id = Section.objects.get(id=dict['object_2_id']).section_id
                dict['object_2_content_type'] = 'section'

            del dict['object_1_id']
            del dict['object_2_id']
            pref_data = list(dict.values())
            pref_data.extend([object_1_natural_id, object_2_natural_id])
            rows.append(pref_data)
        else:
            rows.append(list(obj['fields'].values()))

    response = write_to_csv(rows, cols, HttpResponse(content_type='text/csv'))
    response['Content-Disposition'] = u'attachment; filename="{}"'.format(filename)
    return response
