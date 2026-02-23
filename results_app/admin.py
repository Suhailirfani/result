from django.contrib import admin
from .models import Institution, Student, Subject, Result

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_institutions']
    
    def approve_institutions(self, request, queryset):
        queryset.update(is_approved=True)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'fathers_name', 'register_number', 'student_class', 'institution')
    search_fields = ('name', 'fathers_name', 'register_number')
    list_filter = ('institution', 'student_class')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class', 'institution')
    list_filter = ('institution', 'student_class')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    search_fields = ('student__name', 'student__register_number', 'subject__name')
    list_filter = ('subject__student_class', 'subject')
