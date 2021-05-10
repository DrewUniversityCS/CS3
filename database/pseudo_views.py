from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render
from accounts.models import BaseUser
from database.models.user_models import Teacher


def load_dropdown_options(request):
    content_type_id = request.GET.get('content_type_id')
    content_type = ContentType.objects.get_for_id(content_type_id)
    if content_type == ContentType.objects.get(app_label="accounts", model="baseuser"):
        teachers = Teacher.objects.all()
        options = BaseUser.objects.filter(Q(teacher__in=teachers))
    else:
        options = content_type.get_all_objects_for_this_type()

    return render(request, 'components/dropdown_list_options.html', {'queryset': options})
