from datetime import datetime
from functools import update_wrapper

from django.db.models.fields.related import ManyToManyField
from django.core.serializers import json, serialize
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from university.models import Exam as currentModel
from university.models import student as StudentModel
from Polytech import customviews

class Exams(customviews.JsonView):
    model = currentModel

    def get_context_data(self, **kwargs):
        #context = super(Exams, self).get_context_data(**kwargs)
        context = {}
        exams = self.model.objects.all()

        ##############
        # Filter By Student or Group
        ##############

        if 'group' in self.request.GET or 'student' in self.request.GET:
            if 'student' in self.request.GET:
                exams.filter(student=self.request.GET.get('student'))
            else:
                exams.filter(group=self.request.GET.get('group'))

        ##############
        # Filter By Exam Type
        ##############

        if 'type' in self.request.GET:
            exams.filter(type=self.request.GET.get('type'))

        ##############
        # Filter By Date
        ##############

        if 'date' in self.request.GET:
            if self.request.GET.get('date') == 'next':
                exams = exams.filter(date__gte=datetime.now())
            else:
                if 'from' in self.request.GET:
                    print(self.request.GET.get('from'))
                    exams = exams.filter(date__gte=self.request.GET.get('from'))
                if 'to' in self.request.GET:
                    print(self.request.GET.get('to'))
                    exams = exams.filter(date__lte=self.request.GET.get('to'))

        context['exams'] = []
        for exam in exams:
            diction = {}
            diction['id'] = int(exam.id)
            diction['subject'] = str(exam.subject.name)
            diction['group'] = str(exam.group.name)
            diction['type'] = str(exam.type.name)
            diction['date'] = str(exam.date)
            context['exams'].append(diction)
        return context

class GetExam(customviews.JsonModelView):
    model = currentModel

    def get_context_data(self, **kwargs):
        context = {}
        context['exam'] = []
        diction = {}
        exam = self.modelObject
        diction['id'] = int(exam.id)
        diction['subject'] = str(exam.subject.name)
        diction['group'] = str(exam.group.name)
        diction['type'] = str(exam.type.name)
        diction['date'] = str(exam.date)
        diction['lacturer'] = str(exam.lacturer.fullname)
        context['exam'].append(diction)

        return context

class Student(customviews.JsonModelView):
    model = StudentModel

    def get_context_data(self, **kwargs):
        context = {}
        context['details'] = []
        context['StudentExist'] = True
        diction = {}
        print(self.get)
        student_instance = self.modelObject
        diction['id'] = int(student_instance.id)
        diction['firstname'] = str(student_instance.firstName)
        diction['lastname'] = str(student_instance.lastName)
        diction['group'] = str(student_instance.group.name)
        diction['email'] = str(student_instance.email)
        context['details'].append(diction)
        return context