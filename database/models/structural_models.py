from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModelSet(models.Model):
    """
    A model to represent a set of objects.
    Used by:
        (1) Courses to represent a group of courses (for example the set of classes that is sent to gather student
            interest)
        (2) Sets of preferences to group them for convenience sake.
    """
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class SetMembership(models.Model):
    """
    A model to represent that a given model belongs to the given model set.
    """
    set = models.ForeignKey(ModelSet, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    member_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.member_object) + " is member of " + str(self.set)


class Preference(models.Model):
    """
    True: Positive Preference (I.e 2 classes must be offered at the same time)
    False: Negative Preference (I.e 2 classes have to be offered at different times)
    """
    weight = models.BooleanField()

    """
    Possible Constraint Expressions:
        - Course / Other Course
            - Course overlaps and pre/co requisites are expressed this way.
        - Course / User 
            - Does a teacher / student want to teach / take the class.
        - Course / Timeblock
            - A course should / should not be offered during a timeblock.
        - Course / Other Course / Timeblock
            - The following two classes cannot be offered during the same timeblock.
        - User (Teacher) / Timeblock
            - The given user needs to / can't teach a class during the given timeblock.        
    """
    course = models.ForeignKey("database.Course", on_delete=models.CASCADE, null=True, blank=True)
    other_course = models.ForeignKey("database.Course", on_delete=models.CASCADE, related_name="other course+")
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, null=True, blank=True)
    timeblock = models.ForeignKey("database.Timeblock", on_delete=models.CASCADE)

    sets = GenericRelation(SetMembership, related_query_name='preference')

    class Meta:
        verbose_name_plural = "preferences"


class Department(models.Model):
    """
    An academic department.
    """
    abbreviation = models.CharField(max_length=4, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name + ": " + self.abbreviation

    def natural_key(self):
        return self.name
