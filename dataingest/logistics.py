import codecs
from csv import DictReader, writer

from accounts.models import BaseUser
from database.models.schedule_models import Course
from database.models.structural_models import Preference, Department
from database.models.user_models import Student


required_course_fields = ['department', 'name', 'number']
required_student_fields = ['student_id', 'class_standing', 'first_name', 'last_name', 'email']
required_preference_fields = ['object_1_content_type', 'object_1', 'object_2_content_type', 'object_2']


def create_courses(file):
    shipback = []
    r = DictReader(codecs.iterdecode(file, 'utf-8'))
    for row in r:
        department = Department.objects.get(name=row['department'])
        shipback.append(Course(
            department=department,
            name=row['name'],
            number=int(row['number']),
            credit_hours=int(row['credit_hours']),
            comments=row['comments'],
            offered_annually=bool(row['offered_annually'])
        ))
    return shipback


def create_students(file):
    users_shipback = []
    students_shipback = []
    r = DictReader(codecs.iterdecode(file, 'utf-8'))
    for row in r:
        user_object = BaseUser(
            id=BaseUser.objects.order_by('id').first().id + 1,  # next available id
            username=row["email"].split("@")[0],
            email=row["email"],
            password=BaseUser.objects.make_random_password(),
            first_name=row["first_name"],
            last_name=row["last_name"]
        )

        student_object = Student(
            student_id=row["student_id"],
            class_standing=row["class_standing"],
            user=user_object,
            user_id=user_object.id
        )

        users_shipback.append(user_object)
        students_shipback.append(student_object)
    return users_shipback, students_shipback


def create_preferences(file):
    shipback = []
    r = DictReader(codecs.iterdecode(file, 'utf-8'))
    for row in r:
        shipback.append(Preference(
            # TODO
        ))
    return shipback


def write_to_csv(rows, cols, response):
    w = writer(response)
    w.writerow(cols)
    w.writerows(rows)
    return response
