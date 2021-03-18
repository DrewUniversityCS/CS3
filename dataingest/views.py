from csv import reader
from io import TextIOWrapper

from django.shortcuts import render, redirect

from .forms import CSVForm
from .models import CSV


def upload(request):
    if request.method == 'POST':
        f = TextIOWrapper(request.FILES['document'].file, encoding=request.encoding)
        r = reader(f, delimiter=',')
        for row in r:
            print(row)
    return render(request, 'dataingest/upload.html')


def csv_list(request):
    csvs = CSV.objects.all()
    return render(request, 'dataingest/csv_list.html', {
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
    return render(request, 'dataingest/upload_csv.html', {
        'form': form
    })
