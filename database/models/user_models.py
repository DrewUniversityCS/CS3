from django.db import models

from database.reliability.enums import YEAR_IN_SCHOOL_CHOICES
from database.reliability.validators import student_id_validator


class Student(models.Model):
    """
    The student data model.
    """
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, blank=False, null=False)
    student_id = models.IntegerField(unique=True, validators=[student_id_validator])
    class_standing = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)

    def __str__(self):
        return self.user.get_full_name() + ', ' + self.class_standing + ' : ' + str(self.student_id)

    def is_upperclassman(self):
        return self.class_standing in {YEAR_IN_SCHOOL_CHOICES.JUNIOR, YEAR_IN_SCHOOL_CHOICES.SENIOR}

    def is_senior(self):
        return self.class_standing == YEAR_IN_SCHOOL_CHOICES.SENIOR


class Teacher(models.Model):
    """
    The teacher / instructor data model.
    """
    user = models.ForeignKey("accounts.BaseUser", on_delete=models.CASCADE, blank=False, null=False)
    overseeing_department = models.ForeignKey("database.Department", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() + ', ' + self.overseeing_department.name
