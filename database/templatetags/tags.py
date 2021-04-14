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


@register.simple_tag()
def get_course_stats(form):
    stats_list = []
    courses = Course.objects.filter(sets__set=form.course_set)
    for course in courses:
        stats_list.append({
            'course': course,
            'count': form.entries.filter(courses=course).count()
        })

    return stats_list


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
