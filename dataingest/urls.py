from django.urls import path

from dataingest.views import UploadCSVFileView, DownloadCSVFileView, download_as_csv, UploadCSVFileSuccessView

urlpatterns = [
    path("dataingest/upload/", UploadCSVFileView.as_view(), name="upload_csv"),
    path("dataingest/upload/success", UploadCSVFileSuccessView.as_view(), name="upload_csv_success"),
    path("dataingest/download/<slug:model>/<slug:id>", DownloadCSVFileView.as_view(), name="download_csv"),
    path("dataingest/download_csv/", download_as_csv, name="download_as_csv")
]

app_name = 'dataingest'
