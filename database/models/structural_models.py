from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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


class PreferenceForm(models.Model):
    """
    Keeps Track of preference form Open for a set.
    """
    set = models.ForeignKey(ModelSet, on_delete=models.CASCADE)
    is_taking_responses = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.set} --> {self.is_taking_responses}'


class PreferenceFormEntry(models.Model):
    """
    Keeps Student preference entries
    """
    preference_form = models.ForeignKey(PreferenceForm, on_delete=models.CASCADE)
    student_name = models.CharField('Student Name', max_length=100)
    email = models.EmailField('Student Email')
    courses = models.ManyToManyField('Course')

    def __str__(self):
        return f'{self.student_name}({self.email}) - {self.preference_form.set}'


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


class Building(models.Model):
    """
    A building classes may be offered in.
    """
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name


class Room(models.Model):
    """
    A specific room a class can be offered in. Contained in a building.
    """
    number = models.IntegerField(blank=True, null=True)
    building = models.ForeignKey("database.Building", on_delete=models.CASCADE, related_name="rooms+")

    def __str__(self):
        return self.building.name + " " + str(self.number)
