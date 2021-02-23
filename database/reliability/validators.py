"""
File Name: Validators
Purpose: Functions for verifying that database data is in an acceptable format.
Comments:
"""
from django.core.exceptions import ValidationError


def student_id_validator(sid):
    """
    This validator will ensure that the provided id number is
    (1) 7 digits long
    Otherwise it raises a validation error.
    :param sid: student id being tested
    :return: None
    """
    if len(str(sid)) != 7:
        raise ValidationError("Student ID must be 7 digits long.")
