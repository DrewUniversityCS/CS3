from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import CSVForm
from .models import CSV

class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
        print(uploaded_file.read)
        print("doing something")
    return render(request, 'upload.html')


def csv_list(request):
    csvs = CSV.objects.all()
    return render(request, 'csv_list.html', {
        'csvs': csvs
    })


def upload_csv(request):
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('csv_list')
    else:
        form = CSVForm()
    return render(request, 'upload_csv.html', {
        'form': form
    })

