from django import template
from django.template.defaultfilters import stringfilter

from database.enums import FALL, WINTER, SPRING, SUMMER, SEASONS, YEAR_IN_SCHOOL_CHOICES, FRESHMAN, SOPHOMORE, SENIOR, \
    JUNIOR, GRADUATE
from database.models.schedule_models import Course

register = template.Library()


@register.filter
@stringfilter
def parse_var(value):
    value = value.replace('_', ' ')
    value = value.capitalize()
    return value


@register.filter
@stringfilter
def get_timeblock_letter(value):
    return value[0]


@register.filter
@stringfilter
def parse_time(value):
    id_letter = value[0]  # will return the letter name of the block
    if id_letter == 'A':
        return '7:45 AM - 8:50 AM'
    elif id_letter == 'B':
        return '8:00 AM - 8:50 AM'
    elif id_letter == 'C':
        return '09:00 AM - 10:15 AM'
    elif id_letter == 'D':
        return '09:00 AM - 10:15 AM'
    elif id_letter == 'E':
        return '10:25 AM - 11:40 AM'
    elif id_letter == 'F':
        return '10:25 AM - 11:40 AM'
    elif id_letter == 'G':
        return '11:50 AM - 01:05 PM'
    elif id_letter == 'H':
        return '11:50 AM - 01:05 PM'
    elif id_letter == 'J':
        return '01:15 PM - 02:30 PM'
    elif id_letter == 'K':
        return '01:15 PM - 02:30 PM'
    elif id_letter == 'L':
        return '04:30 PM - 05:45 PM'
    elif id_letter == 'M':
        return '04:30 PM - 05:45 PM'
    elif id_letter == 'P':
        return '07:00 PM - 09:30 PM'
    elif id_letter == 'Q':
        return '07:00 PM - 09:30 PM'
    elif id_letter == 'R':
        return '07:00 PM - 09:30 PM'
    elif id_letter == 'S':
        return '07:00 PM - 09:30 PM'
    elif id_letter == 'T':
        return '02:40 PM - 03:55 PM'
    elif id_letter == 'Z':
        return '02:40 PM - 03:55 PM'

    return value


@register.filter
@stringfilter
def clean_preference_field_name(value):
    if value == 'Weight':
        return 'Positive?'
    elif value == 'Object 1 content type':
        return 'Member A Type'
    elif value == 'Object 2 content type':
        return 'Member B Type'
    elif value == 'Object 1 id':
        return 'Member A Data'
    elif value == 'Object 2 id':
        return 'Member B Data'
    return value


@register.filter
@stringfilter
def to_human_readable(value):
    if value in [FALL, WINTER, SPRING, SUMMER]:
        # The line below is from the following gist:
        # https://gist.github.com/particledecay/4955644
        return [choice[1] for choice in SEASONS if value in choice][0]
    elif value in [FRESHMAN, SOPHOMORE, JUNIOR, SENIOR, GRADUATE]:
        return [choice[1] for choice in YEAR_IN_SCHOOL_CHOICES if value in choice][0]
    elif str(value) and value[0] == '(':
        if value == "('accounts', 'baseuser')":
            return "Teacher"
        elif value == "('database', 'timeblock')":
            return "Timeblock"
        elif value == "('database', 'course')":
            return "Course"
    return value


@register.filter
@stringfilter
def obj_to_dynamic_model_name(value):
    if value == 'database | course':
        return 'courses'
    elif value == 'database | student':
        return 'students'
    elif value == 'database | preference':
        return 'preferences'
    return value


@register.filter
@stringfilter
def set_type_to_color(param):
    if param == 'database | course':
        return 'green-500'
    elif param == 'database | student':
        return 'blue-500'
    elif param == 'database | preference':
        return 'red-500'
    return param


@register.simple_tag()
def get_course_stats(form, total):
    stats_list = []
    courses = Course.objects.filter(sets__set=form.course_set)
    for course in courses:
        stats_list.append({
            'course': course,
            'count': form.entries.filter(courses=course).count()/(total*1.00)*100
        })

    return stats_list


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
