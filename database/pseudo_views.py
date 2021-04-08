from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# AJAX


def load_dropdown_options(request):
    content_type_id = request.GET.get('content_type_id')
    content_type = ContentType.objects.get_for_id(content_type_id)
    options = content_type.get_all_objects_for_this_type()

    return render(request, 'components/dropdown_list_options.html', {'queryset': options})
