import codecs
from csv import DictReader, writer

from django.contrib.contenttypes.models import ContentType

from accounts.models import BaseUser
from database.models.schedule_models import Course, Timeblock
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

        obj_1_id = -1
        if row['object_1_content_type'] == 'course':
            obj_1_id = Course.objects.get(name=row['object_1_natural_id']).id
        elif row['object_1_content_type'] == 'teacher':
            obj_1_id = BaseUser.objects.get(email=row['object_1_natural_id']).id
            row['object_1_content_type'] = 'baseuser'  # so we get the appropriate content type later

        obj_2_id = -1
        if row['object_2_content_type'] == 'course':
            obj_2_id = Course.objects.get(name=row['object_2_natural_id']).id
        elif row['object_2_content_type'] == 'timeblock':
            obj_2_id = Timeblock.objects.get(block_id=row['object_2_natural_id']).id

        shipback.append(Preference(
            weight=row["weight"],
            object_1_content_type=ContentType.objects.filter(model=row['object_1_content_type'])[0],
            object_2_content_type=ContentType.objects.filter(model=row['object_2_content_type'])[0],
            object_1_id=obj_1_id,
            object_2_id=obj_2_id
        ))
    return shipback


def write_to_csv(rows, cols, response):
    w = writer(response)
    w.writerow(cols)
    w.writerows(rows)
    return response
