from django.shortcuts import render

from database.forms import DepartmentForm
from database.models.structural_models import Department


def department_crud(request):
    template_name = "crud/generic_crud_view.html"
    all_objects = Department.objects.all()
    form = DepartmentForm()
    return render(request, template_name, {"all_objects": all_objects, "form": form})
