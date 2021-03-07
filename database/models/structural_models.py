from django.db import models


class Department(models.Model):
    """
    An academic department.
    """
    abbreviation = models.CharField(max_length=4, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    department_head = models.ForeignKey("database.Teacher", on_delete=models.CASCADE,
                                        related_name="department supervised+")

    def __str__(self):
        return self.name + ": " + self.abbreviation


class Building(models.Model):
    """
    A building classes may be offered in.
    """
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    """
    A specific room a class can be offered in. Contained in a building.
    """
    number = models.IntegerField(blank=True, null=True)
    building = models.ForeignKey("database.Building", on_delete=models.CASCADE, related_name="rooms+")
    max_occupancy = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.building.name + " " + str(self.number)
