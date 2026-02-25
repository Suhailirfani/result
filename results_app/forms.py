from django import forms
from django.contrib.auth.models import User
from .models import Student, Subject, Result, Institution, Exam

class InstitutionRegistrationForm(forms.ModelForm):
    institution_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Adabiyya High School'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9947924613'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class StudentSearchForm(forms.Form):
    register_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Register Number'}))

class SingleUploadForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'exam', 'marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BulkUploadForm(forms.Form):
    exam_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Model Exam 2026'}))
    file = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'}))

class StudentBulkUploadForm(forms.Form):
    file = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'}))

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'fathers_name', 'register_number', 'student_class', 'division']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student Name'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Father's Name"}),
            'register_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Register Number'}),
            'student_class': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5'}),
            'division': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g. A"}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'student_class']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mathematics'}),
            'student_class': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5'}),
        }

class InstitutionEditForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Model Exam 2026'}),
        }
