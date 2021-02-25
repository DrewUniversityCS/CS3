from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

#### Course Preferences ################################################################################################


class AbstractCoursePreference(models.Model):
    """
    Base relationship to represent course preferences.
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CourseOverlapPreference(AbstractCoursePreference):
    """
    Relationship for specifying if two classes can or cannot be offered at the same time.
    """
    other_course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="other course+")
    # Weight explanation:
    # -1.0 : the two courses should never overlap.
    # -0.5 : the courses should preferably not overlap.
    # 0.0 : same as a non-existing relationship.
    # 0.5 : the courses should overlap if possible.
    # 1.0: the courses should always overlap (this is the default for cross listed classes for example)
    weight = models.FloatField(null=False, blank=False, default=0.0,
                               validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])


class TeacherCoursePreference(AbstractCoursePreference):
    """
    Relationship for specifying how much a teacher wants to teach a particular class.
    """
    teacher = models.ForeignKey("database.Teacher", on_delete=models.CASCADE)
    # Weight explanation:
    # -1.0 : the teacher should never teach the given course.
    # -0.5 : the teacher would like not to teach this course (non-mandatory, but preferable).
    # 0.0 : same as a non-existing relationship.
    # 0.5 : the teacher would like to teach this course (non-mandatory, but preferable).
    # 1.0: the teacher should always teach the given course.
    weight = models.FloatField(null=False, blank=False, default=0.0,
                               validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])


class StudentCoursePreference(AbstractCoursePreference):
    """
    Relationship for specifying how much a student wants to take a given class.
    """
    student = models.ForeignKey("database.Student", on_delete=models.CASCADE)
    # Weight explanation:
    # 0.0 : same as a non-existing relationship.
    #       We do not have negative weights here because we don't care what classes students don't want to take.
    # 0.5 : the student would like to take this course (non-mandatory, but preferable).
    # 1.0: the student has to take this course.
    weight = models.FloatField(null=False, blank=False, default=0.5,
                               validators=[MinValueValidator(0), MaxValueValidator(1.0)])


class CourseRoomPreference(AbstractCoursePreference):
    """
    Relationship for specifying if a course should / should not be offered in a particular room.
    """
    room = models.ForeignKey("database.Room", on_delete=models.CASCADE)
    # Weight explanation:
    # -1.0 : the course should never be in this room.
    # -0.5 : the course should preferably be somewhere else.
    # 0.0 : same as a non-existing relationship.
    # 0.5 : it would be nice if the course was offered in this room.
    # 1.0: the course has to be offered in this room.
    weight = models.FloatField(null=False, blank=False, default=0.0,
                               validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])


class CourseTimeBlockPreference(AbstractCoursePreference):
    """
    Relationship for specifying if a course should / should not be offered during a particular timeblock.
    """
    timeblock = models.ForeignKey("database.TimeBlock", on_delete=models.CASCADE)
    # Weight explanation:
    # -1.0 : the course should never happen during this time.
    # -0.5 : the course should not happen during this time.
    # 0.0 : same as a non-existing relationship.
    # 0.5 : it would be nice if the course was offered during this time.
    # 1.0: the course has to be offered during this timeblock.
    weight = models.FloatField(null=False, blank=False, default=0.0,
                               validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])

#### Teacher Preferences ###############################################################################################


class AbstractTeacherPreference(models.Model):
    """
    Base relationship to represent teacher preferences.
    """
    teacher = models.ForeignKey("database.Teacher", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TeacherRoomPreference(AbstractTeacherPreference):
    """
    Relationship for specifying how much a teacher would like to teach in a given room.
    """
    room = models.ForeignKey("database.Room", on_delete=models.CASCADE)
    # Weight explanation:
    # -1.0 : the teacher should never teach in this room.
    # -0.5 : the teacher preferably wants to teach elsewhere.
    # 0.0 : same as a non-existing relationship.
    # 0.5 : it would be nice if the teacher could teach in this room.
    # 1.0: the teacher has to teach in this room.
    weight = models.FloatField(null=False, blank=False, default=0.0,
                               validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])


class TeacherTimeBlockPreference(AbstractTeacherPreference):
    """
    Relationship for specifying how much a teacher would like to teach at a given time.
    """
    timeblock = models.ForeignKey("database.TimeBlock", on_delete=models.CASCADE)
    # Weight explanation:
    # -1.0 : the teacher should not teach during this time.
    # -0.5 : the teacher would prefer a different timeblock.
    # 0.0 : same as a non-existing relationship.
    # 0.5 : it would be nice if the teacher could teach during this time.
    # 1.0: the teacher has to teach during this time.
    weight = models.FloatField(null=False, blank=False, default=0.0,
                               validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])
