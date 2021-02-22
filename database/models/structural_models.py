from django.db import models


class Department(models.Model):
    abbreviation = models.CharField(max_length=4, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False, primary_key=True)
    department_head = models.ForeignKey("database.Teacher", on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ": " + self.abbreviation


class Building(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, primary_key=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField(blank=True, null=True)
    building = models.ForeignKey("database.Building", on_delete=models.CASCADE)
    max_occupancy = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.building.name + " " + str(self.number)
