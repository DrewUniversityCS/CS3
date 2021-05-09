from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from database.enums import YEAR_IN_SCHOOL_CHOICES
from database.models.structural_models import SetMembership
from database.validators import student_id_validator


class Student(models.Model):
    """
    The student data model.
    """
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, blank=False, null=False)
    student_id = models.IntegerField(unique=True, validators=[student_id_validator], null=True, blank=True)
    class_standing = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, null=True, blank=True)

    sets = GenericRelation(SetMembership, related_query_name='student')

    def __str__(self):
        return self.user.email

    def is_upperclassman(self):
        return self.class_standing in {YEAR_IN_SCHOOL_CHOICES.JUNIOR, YEAR_IN_SCHOOL_CHOICES.SENIOR}

    def is_senior(self):
        return self.class_standing == YEAR_IN_SCHOOL_CHOICES.SENIOR

    def natural_key(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    """
    The teacher / instructor data model.
    """
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, blank=False, null=False)
    department = models.ForeignKey("database.Department", on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        if self.department is None:
            return self.user.get_full_name()
        return self.user.get_full_name() + ', ' + self.department.name

    def natural_key(self):
        return self.user.get_full_name()
