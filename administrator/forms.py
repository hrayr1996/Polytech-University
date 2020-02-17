from django import forms

from university import models
from university.models import student, ambion, fakultet, group, matyan, subject


class addStudent(forms.ModelForm):

    class Meta:
        model = student
        fields = ['firstName', 'lastName', 'hayranun', 'group', 'birthday', 'joindate', 'email']

class Ambion(forms.ModelForm):

    class Meta:
        model = ambion
        fields = ['name', 'shortname', 'varich', 'teachers']
        widgets = {
            'varich' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'teachers' : forms.SelectMultiple(attrs={'class': 'select2_multiple form-control'}),
            'shortname' : forms.TextInput(attrs={'class': 'form-control'}),
            'name' : forms.TextInput(attrs={'class': 'form-control'})
        }

class Fakultet(forms.ModelForm):

    class Meta:
        model = fakultet
        fields = ['name', 'shortname', 'dekan']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'shortname' : forms.TextInput(attrs={'class': 'form-control'}),
            'dekan' : forms.Select(attrs={'class': 'select2_single form-control'})
        }

class Group(forms.ModelForm):

    class Meta:
        model = group
        fields = ['name', 'profession', 'created', 'lecturers']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'profession' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'created' : forms.DateInput(attrs={'class': 'form-control'}),
            'lecturers' : forms.SelectMultiple(attrs={'class': 'select2_multiple form-control'}),
        }

class Matyan(forms.ModelForm):

    class Meta:
        model = matyan
        fields = ['student', 'group', 'loose', 'minute', 'date']
        widgets = {
            'date' : forms.DateInput(attrs={'class': 'form-control'}),
            'student' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'group' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'minute' : forms.NumberInput(attrs={'class': 'form-control'}),
            'loose' : forms.CheckboxInput(attrs={'class': 'form-control'})
        }

class Points(forms.ModelForm):

    class Meta:
        model = models.Points
        fields = ['value', 'student', 'type', 'exam']
        widgets = {
            'student' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'exam' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'type' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'value' : forms.NumberInput(attrs={'class': 'form-control'})
        }

class Profession(forms.ModelForm):

    class Meta:
        model = models.profession
        fields = ['name', 'fakultet', 'years', 'heraka', 'subjects']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'fakultet' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'subjects' : forms.SelectMultiple(attrs={'class': 'select2_multiple form-control'}),
            'years' : forms.NumberInput(attrs={'class': 'form-control'}),
            'heraka' : forms.CheckboxInput(attrs={'class': 'form-control'})
        }

class Staff(forms.ModelForm):

    class Meta:
        model = models.staff
        fields = ['fullname', 'workstarteddate', 'type']
        widgets = {
            'fullname' : forms.TextInput(attrs={'class': 'form-control'}),
            'type' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'workstarteddate' : forms.DateInput(attrs={'class': 'form-control'})
        }

class Student(forms.ModelForm):

    class Meta:
        model = student
        fields = ['firstName', 'lastName', 'hayranun', 'group', 'birthday', 'joindate', 'email', 'phone', 'studyprice', 'petpatver', 'image']
        widgets = {
            'firstName' : forms.TextInput(attrs={'class': 'form-control'}),
            'lastName' : forms.TextInput(attrs={'class': 'form-control'}),
            'hayranun' : forms.TextInput(attrs={'class': 'form-control'}),
            'group' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'birthday' : forms.DateInput(attrs={'class': 'form-control'}),
            'joindate' : forms.DateInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'phone' : forms.NumberInput(attrs={'class': 'form-control'}),
            'studyprice' : forms.NumberInput(attrs={'class': 'form-control'}),
            'petpatver' : forms.CheckboxInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class Subject(forms.ModelForm):

    class Meta:
        model = subject
        fields = ['name', 'lecturers', 'course', 'lessons']
        widgets = {
            'lecturers' : forms.SelectMultiple(attrs={'class': 'select2_multiple form-control'}),
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'course' : forms.NumberInput(attrs={'class': 'form-control'}),
            'lessons' : forms.NumberInput(attrs={'class': 'form-control'})
        }

class Exam(forms.ModelForm):

    class Meta:
        model = models.Exam
        fields = ['subject', 'group', 'type', 'date', 'lacturer']
        widgets = {
            'subject' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'group' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'type' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'lacturer' : forms.Select(attrs={'class': 'select2_single form-control'}),
            'date' : forms.DateInput(attrs={'class': 'form-control'})
        }