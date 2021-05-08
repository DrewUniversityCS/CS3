from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ScheduleDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/schedule-documentation.html'

class DBDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/database-documentation.html'

class DatasheetDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/datasheet-documentation.html'

class DbUpDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/databaseUp-documentation.html'

class StudentDataDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/studentData-documentation.html'


