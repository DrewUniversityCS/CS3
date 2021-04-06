from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.views.generic import FormView

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
