from django import forms
from django.contrib.auth.models import User
from .models import Student, Subject, Result, Institution

class InstitutionRegistrationForm(forms.ModelForm):
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
