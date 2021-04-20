import csv

from database.models.schedule_models import Course
from database.models.structural_models import Preference
from database.models.user_models import Student


required_course_fields = ['department', 'name', 'number']
required_student_fields = ['student_id', 'class_standing', 'first_name', 'last_name', 'email']
required_preference_fields = ['object_1_content_type', 'object_1', 'object_2_content_type', 'object_2']


def create_courses(reader):
    shipback = []
    for row in reader:
        print(row)
        shipback.append(Course.objects.get_or_create(
            department=row['department'],
            name=row['name'],
            number=row['number']
        ))
    return shipback


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
