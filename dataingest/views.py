from django.views.generic import FormView

from .forms import DataForm


class DataView(FormView):
    template_name = 'pages/upload.html'
    form_class = DataForm
    success_url = '/upload'

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)
