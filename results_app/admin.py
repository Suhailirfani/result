from django.contrib import admin
from .models import Student, Subject, Result

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'fathers_name', 'register_number', 'student_class')
    search_fields = ('name', 'fathers_name', 'register_number')
    list_filter = ('student_class',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class')
    list_filter = ('student_class',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    search_fields = ('student__name', 'student__register_number', 'subject__name')
    list_filter = ('subject__student_class', 'subject')
