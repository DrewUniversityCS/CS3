from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView

from database.forms import EmptyForm
from database.models.structural_models import SetMembership, ModelSet
from database.views import DynamicModelMixin
from dataingest.forms import UploadCSVFileForm
from dataingest.logistics import create_courses, create_students, create_preferences


class UploadCSVFileView(LoginRequiredMixin, FormView):
    template_name = 'dataingest/upload_csv_file.html'
    form_class = UploadCSVFileForm
    success_url = '/'

    def form_valid(self, form):
        category = form.data['category']
        file = self.request.FILES['file']

        data_set = file.read().decode('UTF-8')
        r = StringIO(data_set)

        objects = []
        if category == 'course':
            objects = create_courses(r)
        elif category == 'student':
            objects = create_students(r)
        elif category == 'preference':
            objects = create_preferences(r)

        self.request.session['objects'] = serialize('json', objects)

        return HttpResponseRedirect(self.get_success_url())


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

        context['field_data'] = serialize("python", objs, use_natural_foreign_keys=True)
        context['object'] = f"{ModelSet.objects.get(id=set_id)} - {self.dynamic_model.__name__}s"
        return context


def download_as_csv(request):
    # TODO
    file = ''
    response = HttpResponse(file, content_type='text/csv')
    response['Content-Disposition'] = u'attachment; filename="{0}"'.format('export.csv')
    return response
