from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    class_preferences = models.ManyToManyField("database.Course", through="database.CoursePreference")
    room_preferences = models.ManyToManyField("database.Room", through="database.RoomPreference")
    time_preferences = models.ManyToManyField("database.Timeblock", through="database.TimeblockPreference")

    def __str__(self):
        if self.email == "":
            return self.username
        else:
            return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name
