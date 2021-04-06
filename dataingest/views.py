from csv import reader
from io import TextIOWrapper

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from dataingest.forms import UploadCSVFileForm


def upload(request):
    if request.method == 'POST':
        f = TextIOWrapper(request.FILES['document'].file, encoding=request.encoding)
        r = reader(f, delimiter=',')
        for row in r:
            print(row)
    return render(request, 'dataingest/upload_csv_file.html')


class UploadCSVFileView(LoginRequiredMixin, FormView):
    template_name = 'dataingest/upload_csv_file.html'
    form_class = UploadCSVFileForm
    success_url = '/dataingest/manage'

    def form_valid(self, form):

        return HttpResponseRedirect(self.get_success_url())
