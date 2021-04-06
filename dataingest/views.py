from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from dataingest.forms import UploadCSVFileForm


class UploadCSVFileView(LoginRequiredMixin, FormView):
    template_name = 'dataingest/upload_csv_file.html'
    form_class = UploadCSVFileForm
    success_url = '/'

    def form_valid(self, form):
        print(form.data['category'])
        print(self.request.FILES['file'])
        return HttpResponseRedirect(self.get_success_url())
