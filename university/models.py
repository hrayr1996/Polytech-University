from datetime import datetime

from django.db import models

from MediaManagement.models import Image
from Polytech import settings


class student(models.Model):
    firstName = models.CharField(max_length=36)
    lastName = models.CharField(max_length=72)
    hayranun = models.CharField(max_length=36)
    group = models.ForeignKey('group')
    birthday = models.DateField(blank=True, null=True)
    joindate = models.DateField()
    email = models.CharField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(Image, blank=True, null=True)
    petpatver = models.BooleanField(default=False)
    studyprice = models.IntegerField(default=0)
    phone = models.IntegerField()

    def __str__(self):
        return self.lastName + ' ' + self.firstName + ' ' + self.hayranun

class group(models.Model):
    name = models.CharField(max_length=10)
    profession = models.ForeignKey('profession')
    created = models.DateField(verbose_name='Ստեղծման Տարի')
    lecturers = models.ManyToManyField('staff')

    def __str__(self):
        return self.name

class profession(models.Model):
    name = models.CharField(max_length=255)
    fakultet = models.ForeignKey('fakultet')
    years = models.IntegerField()
    heraka = models.BooleanField(default=False, blank=True, verbose_name='հեռակա')
    subjects = models.ManyToManyField('subject')

    def __str__(self):
        return self.name

class fakultet(models.Model):
    name = models.CharField(max_length=150)
    shortname = models.CharField(max_length=10)
    dekan = models.OneToOneField('staff')

    def __str__(self):
        return self.name


class staff(models.Model):
    fullname = models.CharField(max_length=25)
    workstarteddate = models.DateField(blank=True, null=True)
    type = models.ForeignKey('WorkerType')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'worker'
        verbose_name_plural = 'Workers'

class WorkerType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class subject(models.Model):
    name = models.CharField(max_length=200)
    lecturers = models.ManyToManyField('staff')
    course = models.IntegerField() # Semestr
    lessons = models.IntegerField(verbose_name='Սեմեստրի լեկցիաների քանակը')

    def __str__(self):
        return self.name

class ambion(models.Model):
    name = models.CharField(max_length=150)
    shortname = models.CharField(max_length=50)
    varich = models.OneToOneField('staff', unique=True, related_name='ambionvarich')
    teachers = models.ManyToManyField('staff', related_name='ambionteacher')

    def __str__(self):
        return self.name

class matyan(models.Model):
    student = models.ForeignKey('student')
    group = models.ForeignKey('group')
    loose = models.BooleanField(default=True)
    minute = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.student + ' ' + str(self.minute)

class tareketum(models.Model):
    student = models.ForeignKey('student')
    semestr = models.IntegerField(verbose_name='Տարկետման սեմեստր')
    length = models.IntegerField(verbose_name='Ժամկետ')
    currentgroup = models.ManyToOneRel('self', 'group', field_name="currgroup")

    def __str__(self):
        return self.student + ' - ' + self.semestr + ' - ' + self.length


class Points(models.Model):
    value = models.FloatField()
    student = models.ForeignKey('student')
    type = models.ForeignKey('PointType')
    exam = models.ForeignKey('Exam')

    def __str__(self):
        return self.student + " -> " + self.subject + " == " + self.value

class ExamType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class PointType(models.Model):
    name = models.CharField(max_length=255)

class Exam(models.Model):
    subject = models.ForeignKey(subject)
    group = models.ForeignKey(group)
    type = models.ForeignKey(ExamType)
    date = models.DateField(default=datetime.now())
    lacturer = models.ForeignKey(staff, blank=True, null=True)
    def __str__(self):
        return self.type.name + ' քննություն ' + self.subject.name + ' առարկայից ' + str(self.date) + ' օրը'
