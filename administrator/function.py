import json

from django.http import HttpResponse

from university.models import ambion, Exam, fakultet, group, matyan, Points, profession, staff, student, subject, \
    tareketum

def delete(request, **kwargs):
    items = []
    model = None
    if 'id' in kwargs:
        id = kwargs['id']
        items.append(id)
    if request.method == 'POST':
        items = request.POST.getlist('items[]')
        print(request.POST)
    if 'model' in kwargs:
        if kwargs['model'] == 'ամբիոն':
            model = ambion
        elif kwargs['model'] == 'քննություններ':
            model = Exam
        elif kwargs['model'] == 'ֆակուլտետ':
            model = fakultet
        elif kwargs['model'] == 'խումբ':
            model = group
        elif kwargs['model'] == 'մատյան':
            model = matyan
        elif kwargs['model'] == 'գնահատական':
            model = Points
        elif kwargs['model'] == 'մասնագիտություն':
            model = profession
        elif kwargs['model'] == 'աշխատակազմ':
            model = staff
        elif kwargs['model'] == 'ուսանողներ':
            model = student
        elif kwargs['model'] == 'առարկաներ':
            model = subject
        elif kwargs['model'] == 'տարեկետում':
            model = tareketum
        else:
            model = None
    try:
        model.objects.filter(id__in=items).delete()
        errors = "Success"
    except:
        errors = "Can't delete Items"
    return HttpResponse(json.dumps({'errors':errors}), content_type='application/json')