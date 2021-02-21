from django.db import models


class Course(models.Model):
    department = models.ForeignKey("database.Department", on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    code = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.department.abbreviation + str(self.code)


class Section(models.Model):
    pass


class Schedule(models.Model):
    pass


class Weekday(models.Model):
    pass


class TimeBlock(models.Model):
    pass

