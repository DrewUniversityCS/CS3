from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    class_preferences = models.ManyToManyField("database.Course", through="database.CoursePreference")
    room_preferences = models.ManyToManyField("database.Room", through="database.RoomPreference")
    time_preferences = models.ManyToManyField("database.TimeBlock", through="database.TimePreference")

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name
