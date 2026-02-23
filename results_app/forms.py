from django import forms
from django.contrib.auth.models import User
from .models import Student, Subject, Result, Institution

class InstitutionRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class StudentSearchForm(forms.Form):
    institution = forms.ModelChoiceField(queryset=Institution.objects.filter(is_approved=True), widget=forms.Select(attrs={'class': 'form-control'}))
    register_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Register Number'}))

class SingleUploadForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BulkUploadForm(forms.Form):
    student_class = forms.IntegerField(required=True, min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Class (e.g. 5)'}))
    file = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'}))
