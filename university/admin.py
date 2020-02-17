from django.contrib import admin

from university.models import student, group, profession, fakultet, staff, ambion, WorkerType, subject, ExamType

admin.site.register(student)
admin.site.register(group)
admin.site.register(profession)
admin.site.register(fakultet)
admin.site.register(subject)
admin.site.register(staff)
admin.site.register(ambion)
admin.site.register(WorkerType)
admin.site.register(ExamType)