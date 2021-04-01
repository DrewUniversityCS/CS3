from django.contrib.contenttypes.fields import GenericForeignKey
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
