from django import forms
from django.contrib.auth.models import User
from .models import Student, Subject, Result, Institution, Exam

class InstitutionRegistrationForm(forms.ModelForm):
    institution_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Adabiyya High School'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9947924613'}))
    grading_system = forms.ChoiceField(choices=Institution.GRADING_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    logo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/png, image/jpeg'}))
    
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
    existing_exam = forms.ModelChoiceField(
        queryset=Exam.objects.none(), 
        required=False, 
        empty_label="-- Select an existing exam --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    new_exam_name = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'OR enter a new exam name'})
    )
    file = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'}))

    def __init__(self, *args, **kwargs):
        institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        if institution:
            self.fields['existing_exam'].queryset = Exam.objects.filter(institution=institution).order_by('-id')

    def clean(self):
        cleaned_data = super().clean()
        existing_exam = cleaned_data.get('existing_exam')
        new_exam_name = cleaned_data.get('new_exam_name')

        if not existing_exam and not new_exam_name:
            raise forms.ValidationError("You must either select an existing exam or enter a new exam name.")
        
        return cleaned_data

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
        fields = ['name', 'student_class', 'max_marks']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mathematics'}),
            'student_class': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Default: 100'}),
        }

class InstitutionEditForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'phone_number', 'grading_system', 'results_locked', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'grading_system': forms.Select(attrs={'class': 'form-control'}),
            'results_locked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/png, image/jpeg'}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Model Exam 2026'}),
        }
