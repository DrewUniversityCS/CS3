from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Preference(models.Model):
    weight = models.FloatField(
        null=False,
        blank=False,
        default=0.0,
        validators=[MinValueValidator(-1.0),
                    MaxValueValidator(1.0)]
    )

    class Meta:
        abstract = True
        verbose_name_plural = "preferences"


class CoursePreference(Preference):
    """
    Base relationship to represent course preferences.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.course is None:
            return self.user.get_full_name() + " preference (partial)"
        elif self.user is None:
            return str(self.course) + " preference (partial)"
        else:
            return self.user.get_full_name() + " has a preference of " + str(self.weight) + " with " + str(self.course)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in CoursePreference._meta.fields]

    class Meta:
        verbose_name_plural = "course preferences"


class OverlapPreference(Preference):
    """
    Relationship for specifying if two classes can or cannot be offered at the same time.
    Also used to signify things like prereqs, coreqs and co-listed classes through the value of the preference weight.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE)
    other_course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="other course+")

    def __str__(self):
        return str(self.course) + " has a preference of " + str(self.weight) + " with " + str(self.other_course)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in OverlapPreference._meta.fields]

    class Meta:
        verbose_name_plural = "course overlap preferences"


class RoomPreference(CoursePreference):
    """
    Relationship for signifying room preferences for a course or teacher. If this is a teacher-room preference,
    the course is left blank, and if its a course-room, the user field is left blank.
    """
    room = models.ForeignKey("database.Room", on_delete=models.CASCADE)

    def __str__(self):
        if self.course is None:
            return self.user.get_full_name() + " has a preference of " + str(self.weight) + " with " + str(self.room)
        else:
            return str(self.course) + " has a preference of " + str(self.weight) + " with " + str(self.room)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in RoomPreference._meta.fields]

    class Meta:
        verbose_name_plural = "room preferences"


class TimeblockPreference(CoursePreference):
    """
    Relationship for signifying time preferences for a course or teacher. If this is a teacher-room preference,
    the course is left blank, and if its a course-room, the user field is left blank.
    """
    timeblock = models.ForeignKey("database.Timeblock", on_delete=models.CASCADE)

    def __str__(self):
        if self.course is None:
            return self.user.get_full_name() + " has a preference of " + str(self.weight) + " with " + \
                   str(self.timeblock)
        else:
            return str(self.course) + " has a preference of " + str(self.weight) + " with " + str(self.timeblock)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in TimeblockPreference._meta.fields]

    class Meta:
        verbose_name_plural = "timeblock preferences"


class Registration(models.Model):
    """
    Relationship to signify a students registration for a course section (not necessarily successful)
    """
    section = models.ForeignKey("database.Section", on_delete=models.CASCADE)
    student = models.ForeignKey("database.Student", on_delete=models.CASCADE)
    approval = models.BooleanField(default=False)
    approving_teacher = models.ForeignKey("database.Teacher", on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.get_full_name() + " registration for " + self.section.__str__()

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Registration._meta.fields]

    class Meta:
        verbose_name_plural = "registrations"
