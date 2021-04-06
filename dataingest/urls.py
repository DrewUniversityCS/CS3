from django.urls import path

from dataingest.views import UploadCSVFileView

urlpatterns = [
    path("dataingest/upload/", UploadCSVFileView.as_view(), name="upload_csv")
]

app_name = 'dataingest'
