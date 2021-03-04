from django.db import models

from database.enums import SEASONS, POSSIBLE_HOURS, POSSIBLE_MINUTES


class Course(models.Model):
    """
    Represents a specific course offering. Importantly, this is not something a student takes or an instructor teaches.
    Rather, courses are instantiated in the form of sections.
    """
    department = models.ForeignKey("database.Department", on_delete=models.CASCADE, related_name="courses offered+")
    name = models.CharField(max_length=256, blank=False, null=False)
    number = models.IntegerField(blank=False, null=False)
    CRN = models.IntegerField(blank=False, null=False)
    max_enrollment = models.IntegerField(blank=False, null=True)
    credit_hours = models.IntegerField(default=4)
    comments = models.TextField()

    # Note: overlap preferences is how we express course (1) coreqs, (2) prereqs,
    # (3) overlap blocks, (4) general preferences
    overlap_preferences = models.ManyToManyField("database.Course", through="database.CourseOverlapPreference",
                                                 related_name="overlap preferences+")
    room_preferences = models.ManyToManyField("database.Room", through="database.RoomPreference",
                                              related_name="room preferences+")
    time_preferences = models.ManyToManyField("database.TimeBlock", through="database.TimePreference",
                                              related_name="time preferences+")

    def __str__(self):
        return self.department.abbreviation + str(self.number)


class Section(models.Model):
    """
    An instantiated class offering. Has a particular time and space during which it happens.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="sections+")
    section_id = models.CharField(max_length=4)
    primary_instructor = models.ForeignKey("database.Teacher", on_delete=models.CASCADE,
                                           related_name="sections taught+")
    other_instructor = models.ForeignKey("database.Teacher", on_delete=models.CASCADE,
                                         related_name="sections assisted with+", null=True, blank=True)
    room = models.ForeignKey("database.Room", on_delete=models.CASCADE, related_name="sections+")
    year = models.IntegerField(null=False, blank=False)
    season = models.CharField(choices=SEASONS, max_length=50)
    timeblock = models.ForeignKey("database.TimeBlock", on_delete=models.CASCADE, related_name="sections+")
    schedule = models.ForeignKey("database.Schedule", on_delete=models.CASCADE, related_name="sections+")

    def __str__(self):
        return self.course.name + " " + self.course.department.abbreviation + "-" + str(self.course.number) \
               + " Section " + self.section_id


class Schedule(models.Model):
    """
    A structural model representing a week of classes.
    """
    name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class Weekdays(models.Model):
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


class TimeBlock(models.Model):
    """
    A particular time block during which classes may happen.
    """
    block_id = models.CharField(max_length=32, blank=False, null=False, primary_key=True)
    weekdays = models.ForeignKey("database.Weekdays", on_delete=models.CASCADE, related_name="timeblocks+")
    start_hour = models.IntegerField(choices=POSSIBLE_HOURS)
    start_minutes = models.IntegerField(choices=POSSIBLE_MINUTES)
    end_hour = models.IntegerField(choices=POSSIBLE_HOURS)
    end_minutes = models.IntegerField(choices=POSSIBLE_MINUTES)

    def __str__(self):
        return self.block_id + " " + "(" + str(self.weekdays) + ")"
