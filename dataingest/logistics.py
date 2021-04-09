import csv


def create_courses(reader):
    return []


def create_students(reader):
    return []


def create_preferences(reader):
    return []


def write_to_csv(rows, cols, response):
    writer = csv.writer(response)
    writer.writerow(cols)
    writer.writerows(rows)
    return response
