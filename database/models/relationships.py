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


class CoursePreference(Preference):
    """
    Base relationship to represent course preferences.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, null=True)


class CourseOverlapPreference(Preference):
    """
    Relationship for specifying if two classes can or cannot be offered at the same time.
    Also used to signify things like prereqs, coreqs and co-listed classes through the value of the preference weight.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE)
    other_course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="other course+")


class RoomPreference(CoursePreference):
    """
    Relationship for signifying room preferences for a course or teacher. If this is a teacher-room preference,
    the course is left blank, and if its a course-room, the user field is left blank.
    """
    room = models.ForeignKey("database.Room", on_delete=models.CASCADE)


class TimePreference(CoursePreference):
    """
    Relationship for signifying time preferences for a course or teacher. If this is a teacher-room preference,
    the course is left blank, and if its a course-room, the user field is left blank.
    """
    timeblock = models.ForeignKey("database.TimeBlock", on_delete=models.CASCADE)


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