from csv import reader

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize, deserialize
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView

from database.forms import EmptyForm
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
        file_reader = self.request.FILES['file']
        objects = []
        if category == 'course':
            objects = create_courses(file_reader)
        elif category == 'student':
            objects = create_students(file_reader)
        elif category == 'preference':
            objects = create_preferences(file_reader)

        self.request.session['objects'] = serialize('json', objects)

        return HttpResponseRedirect(self.get_success_url())


class UploadCSVFileSuccessView(LoginRequiredMixin, FormView):
    template_name = "dataingest/upload_verification.html"
    form_class = EmptyForm
    success_url = "/dataingest/upload/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        objects = []
        for obj in deserialize("json", self.request.session.get('objects')):
            objects.append(obj.object)

        context['objects'] = objects
        return context

    def form_valid(self, form):
        if 'confirm' in self.request.POST:
            for obj in deserialize("json", self.request.session.get('objects')):
                obj.object.save()

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

    if 'user' in cols:
        cols.remove('user')
        cols.append('first_name')
        cols.append('last_name')
        cols.append('email')

    rows = []
    for obj in deserialized_objs:
        dict = obj['fields']
        if 'user' in dict:
            user_data = list(dict['user'].values())
            row_data = [dict['student_id'], dict['class_standing']]
            row_data.extend(user_data)
            rows.append(row_data)
        else:
            rows.append(list(obj['fields'].values()))

    response = write_to_csv(rows, cols, HttpResponse(content_type='text/csv'))
    response['Content-Disposition'] = u'attachment; filename="{0}"'.format('export.csv')
    return response
