import string

import django.utils.timezone as timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.crypto import get_random_string

from database.enums import SEASONS, POSSIBLE_HOURS, POSSIBLE_MINUTES
from database.models.structural_models import SetMembership
from database.validators import max_integer_validator
from database.validators import year_validator


class Course(models.Model):
    """
    Represents a specific course offering. Importantly, this is not something a student takes or an instructor teaches.
    Rather, courses are instantiated in the form of sections.
    """
    department = models.ForeignKey("database.Department", on_delete=models.CASCADE, related_name="courses offered+")
    name = models.CharField(max_length=256, blank=False, null=False)
    number = models.IntegerField(blank=False, null=False, validators=[max_integer_validator])
    credit_hours = models.IntegerField(default=4)
    comments = models.TextField(blank=True, null=True)
    offered_annually = models.BooleanField(default=True)

    default_timeblock = models.ForeignKey("database.Timeblock", on_delete=models.CASCADE, null=True, blank=True)
    default_primary_instructor = models.ForeignKey("database.Teacher", on_delete=models.CASCADE, null=True, blank=True)

    sets = GenericRelation(SetMembership, related_query_name='course')

    def __str__(self):
        return self.department.abbreviation + str(self.number)

    def natural_key(self):
        return self.__str__()


class Section(models.Model):
    """
    An instantiated class offering. Has a particular time and space during which it happens.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="sections+")
    section_id = models.CharField(max_length=4, unique=True)
    primary_instructor = models.ForeignKey("database.Teacher", on_delete=models.CASCADE,
                                           related_name="sections taught+", null=True, blank=True)
    other_instructor = models.ForeignKey("database.Teacher", on_delete=models.CASCADE,
                                         related_name="sections assisted with+", null=True, blank=True)

    timeblock = models.ForeignKey("database.Timeblock", on_delete=models.CASCADE, related_name="sections+", blank=True,
                                  null=True)
    schedule = models.ForeignKey("database.Schedule", on_delete=models.CASCADE, related_name="sections+")

    @classmethod
    def create(cls, course, schedule):
        def make_section_id():
            return get_random_string(4, allowed_chars=string.ascii_uppercase + string.digits)

        section = cls(course=course, schedule=schedule, section_id=make_section_id(),
                      timeblock=course.default_timeblock, primary_instructor=course.default_primary_instructor)

        return section

    def __str__(self):
        return self.course.name + " " + self.course.department.abbreviation + "-" + str(self.course.number) \
               + " Section " + self.section_id

    def natural_key(self):
        return self.course.name + " " + self.section_id


class SectionNote(models.Model):

    COLOR_CHOICES = [
        ('#FFFFFF', 'White'),
        ('#C0C0C0', 'Silver'),
        ('#808080', 'Gray'),
        ('#000000', 'Black'),
        ('#FF0000', 'Red'),
        ('#800000', 'Maroon'),
        ('#FFFF00', 'Yellow'),
        ('#808000', 'Olive'),
        ('#00FF00', 'Lime'),
        ('#008000', 'Green'),
        ('#00FFFF', 'Aqua'),
        ('#008080', 'Teal'),
        ('#0000FF', 'Blue'),
        ('#000080', 'Navy'),
        ('#FF00FF', 'Fuchsia'),
        ('#800080', 'Purple'),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    color = models.CharField(choices=COLOR_CHOICES, max_length=7)

    def __str__(self):
        return f'{self.section}-{self.get_color_display()}-{(self.note[:20] + "..") if len(self.note) > 20 else self.note}'


class Schedule(models.Model):
    """
    A structural model representing a week's schedule of classes.
    """
    name = models.CharField(max_length=256, blank=False)
    year = models.IntegerField(default=timezone.now().year, null=False, blank=False, validators=[year_validator])
    season = models.CharField(choices=SEASONS, max_length=50)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.__str__()


class WeekdaySet(models.Model):
    """
    A model to store data on what days a timeblock takes place during.
    """
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)

    def __str__(self):
        if self.monday:
            m = "M"
        else:
            m = ""

        if self.tuesday:
            tu = "Tu"
        else:
            tu = ""

        if self.wednesday:
            w = "W"
        else:
            w = ""

        if self.thursday:
            th = "Th"
        else:
            th = ""

        if self.friday:
            f = "F"
        else:
            f = ""

        return m + tu + w + th + f

    class Meta:
        verbose_name_plural = 'possible weekdays'

    def natural_key(self):
        return self.__str__()


class Timeblock(models.Model):
    """
    A particular time block during which classes may happen.
    """
    block_id = models.CharField(max_length=32, blank=False, null=False, unique=True)
    weekdays = models.ForeignKey("database.WeekdaySet", on_delete=models.CASCADE, related_name="timeblocks+")
    start_hour = models.IntegerField(choices=POSSIBLE_HOURS)
    start_minutes = models.IntegerField(choices=POSSIBLE_MINUTES)
    end_hour = models.IntegerField(choices=POSSIBLE_HOURS)
    end_minutes = models.IntegerField(choices=POSSIBLE_MINUTES)

    def __str__(self):
        def pad(val):
            if len(val) == 1:
                return "0" + val
            else:
                return val

        return self.block_id + " " + "(" + str(self.weekdays) + ")" \
               + " " + pad(str(self.start_hour)) + ":" + pad(str(self.start_minutes)) + \
               " - " + pad(str(self.end_hour)) + ":" + pad(str(self.end_minutes))
