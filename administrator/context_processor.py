from django.urls  import resolve

from university.models import student


def loadContent(request):

    context = {}
    students = student.objects.all()
    for stud in students:
        stud.group.profession.name

    current_url = resolve(request.path_info).url_name
    try:
        if current_url.index('edit') > 0:
            context['is_edit_page'] = True;
    except:
        context['is_edit_page'] = False;
    try:
        if current_url.index('add') > 0:
            context['is_add_page'] = True;
    except:
            context['is_add_page'] = False;

    context['current_url'] = current_url
    return context