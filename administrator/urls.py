from django.conf.urls import url, include
from django.contrib import admin
from administrator.viewpy import Ambion, Fakultet, Group, Matyan, Points, Profession, Staff, Subject, Student, Exam
from administrator import function
from administrator import views
from administrator.views import home, Students

app_name = 'administrator'

urlpatterns = [
    url(r'^$', home.as_view(), name='adminHome'),
    url(r'^ամբիոն', include([
        url(r'^/ավելացնել.html$', Ambion.Add.as_view(), name="add-ambion"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Ambion.Edit.as_view(), name="edit-ambion"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Ambion.List.as_view(), name="list-ambions"),
    ])),
    url(r'^ֆակուլտետ', include([
        url(r'^/ավելացնել.html$', Fakultet.Add.as_view(), name="add-fakultet"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Fakultet.Edit.as_view(), name="edit-fakultet"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Fakultet.List.as_view(), name="list-fakultets"),
    ])),
    url(r'^խումբ', include([
        url(r'^/ավելացնել.html$', Group.Add.as_view(), name="add-group"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Group.Edit.as_view(), name="edit-group"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Group.List.as_view(), name="list-groups"),
    ])),
    url(r'^մատյան', include([
        url(r'^/ավելացնել.html$', Matyan.Add.as_view(), name="add-matyan"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Matyan.Edit.as_view(), name="edit-matyan"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Matyan.List.as_view(), name="list-matyans"),
    ])),
    url(r'^գնահատական', include([
        url(r'^/ավելացնել.html$', Points.Add.as_view(), name="add-point"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Points.Edit.as_view(), name="edit-point"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Points.List.as_view(), name="list-points"),
    ])),
    url(r'^մասնագիտություն', include([
        url(r'^/ավելացնել.html$', Profession.Add.as_view(), name="add-profession"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Profession.Edit.as_view(), name="edit-profession"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Profession.List.as_view(), name="list-professions"),
    ])),
    url(r'^աշխատակազմ', include([
        url(r'^/ավելացնել.html$', Staff.Add.as_view(), name="add-worker"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Staff.Edit.as_view(), name="edit-worker"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Staff.List.as_view(), name="list-staff"),
    ])),
    url(r'^առարկաներ', include([
        url(r'^/ավելացնել.html$', Subject.Add.as_view(), name="add-subject"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Subject.Edit.as_view(), name="edit-subject"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Subject.List.as_view(), name="list-subjects"),
    ])),
    url(r'^ուսանողներ', include([
        url(r'^/ավելացնել.html$', Student.Add.as_view(), name="add-student"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Student.Edit.as_view(), name="edit-student"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Student.List.as_view(), name="list-students"),
    ])),
    url(r'^տարեկետում', include([
        url(r'^/ավելացնել.html$', Subject.Add.as_view(), name="add-tareketum"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Subject.Edit.as_view(), name="edit-tareketum"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Subject.List.as_view(), name="list-tareketum"),
    ])),
    url(r'^քննություններ', include([
        url(r'^/ավելացնել.html$', Exam.Add.as_view(), name="add-exam"),
        url(r'^/(?P<pk>[0-9]+)/խմբագրել.html', Exam.Edit.as_view(), name="edit-exam"),
        url(r'^(?:/ցուցակ)?(?:/page-(?P<page>[0-9]+))?.html', Exam.List.as_view(), name="list-exams"),
    ])),

    url(r'^(?P<model>.*)/ջնջել/(?P<id>[0-9]+).html$', function.delete, name='delete-item-single'),
    url(r'^(?P<model>.*)/ջնջել.html$', function.delete, name='delete-items'),
]
