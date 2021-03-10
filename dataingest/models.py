from django.db import models


class CSV(models.Model):
    CSV_File_Name = models.CharField(max_length=100)
    CSV_File = models.FileField(upload_to='CSVs/files/')

    def __str__(self):
        return self.CSV_File_Name



