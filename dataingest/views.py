from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from csv import reader
from io import TextIOWrapper

from .forms import CSVForm
from .models import CSV


def upload(request):
    if request.method == 'POST':
        f = TextIOWrapper(request.FILES['document'].file, encoding=request.encoding)
        r = reader(f, delimiter=',')
        for row in r:
            print(row)
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
