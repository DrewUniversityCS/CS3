"""
File Name: Validators
Purpose: Functions for verifying that database data is in an acceptable format.
Comments:
"""
from django.core.exceptions import ValidationError
import django.utils.timezone as timezone

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

def year_validator(year):
    """
    This validator will ensure that the provided year is within a reasonable range
    """
    if year>(timezone.now().year+100) or year<(timezone.now().year-100):
        raise ValidationError("Year out of range. Please select a more appropriate range.")

def max_integer_validator(num):
    if len(str(num))>7:
        raise ValidationError("Course number must be less than 7 digits long.")
