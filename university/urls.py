from django.conf.urls import url, include
from django.contrib import admin

from university import views

urlpatterns = [
    url(r'^$', views.home, name='siteHome')
]
