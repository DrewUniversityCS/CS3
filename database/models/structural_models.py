from django.db import models


class Department(models.Model):
    abbreviation = models.CharField(max_length=4, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False, primary_key=True)
    department_head = models.ForeignKey("database.TeacherUser", on_delete=models.CASCADE)


class Building(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, primary_key=True)


class Room(models.Model):
    number = models.IntegerField(blank=True, null=True)
    building = models.ForeignKey("database.Building", on_delete=models.CASCADE)