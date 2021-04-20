import csv

from database.models.schedule_models import Course
from database.models.structural_models import Preference
from database.models.user_models import Student


def create_courses(reader):
    shipback = []
    for row in reader[1:]:
        shipback.append(Course.objects.get_or_create(

        ))
    return []


def create_students(reader):
    shipback = []
    for row in reader[1:]:
        shipback.append(Student.objects.get_or_create(

        ))
    return shipback


def create_preferences(reader):
    shipback = []
    for row in reader[1:]:
        shipback.append(Preference.objects.get_or_create(

        ))
    return shipback


def write_to_csv(rows, cols, response):
    writer = csv.writer(response)
    writer.writerow(cols)
    writer.writerows(rows)
    return response
