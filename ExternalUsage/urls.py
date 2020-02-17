from django.conf.urls import url, include
from django.contrib import admin

from ExternalUsage import views

app_name = 'ExternalUsage'

urlpatterns = [
    url('^exams.json$', views.Exams.as_view(), name='exams-filter-json'),
    url('^exams.json/(?P<pk>[0-9]+)$', views.GetExam.as_view(), name='exams-get-json'),
    url('^student.json/(?P<pk>[0-9]+)$', views.Student.as_view(), name='exams-get-json'),

]
#(?:/(?P<>[a-z]+)?