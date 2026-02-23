from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Subject, Result, Institution, Exam
from .forms import StudentSearchForm, SingleUploadForm, BulkUploadForm, InstitutionRegistrationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db import models
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
import pandas as pd

def register_institution(request):
    if request.method == 'POST':
        form = InstitutionRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Institution.objects.create(user=user, name=user.username)
            auth_login(request, user)
            return redirect('results_app:pending_approval')
    else:
        form = InstitutionRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def pending_approval_view(request):
    if hasattr(request.user, 'institution') and request.user.institution.is_approved:
        return redirect('results_app:staff_dashboard')
    return render(request, 'pending_approval.html')

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('results_app:superadmin_dashboard')
            else:
                return redirect('results_app:staff_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('results_app:home')

@login_required
def superadmin_dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('results_app:home')
    institutions = Institution.objects.all().order_by('is_approved', 'name')
    return render(request, 'superadmin_dashboard.html', {'institutions': institutions})

@login_required
def approve_institution_view(request, inst_id):
    if not request.user.is_superuser:
        return redirect('results_app:home')
    inst = get_object_or_404(Institution, id=inst_id)
    inst.is_approved = not inst.is_approved
    inst.save()
    messages.success(request, f"Institution '{inst.name}' approval status updated.")
    return redirect('results_app:superadmin_dashboard')

def student_result_view(request, inst_id):
    institution = get_object_or_404(Institution, id=inst_id)
    if not institution.is_approved:
        messages.error(request, "This institution's portal is currently inactive.")
        return redirect('results_app:home')
        
    form = StudentSearchForm(request.GET or None)
    results_by_exam = {}
    student = None
    total_marks = 0
    if request.GET and form.is_valid():
        register_number = form.cleaned_data['register_number']
        try:
            student = Student.objects.get(institution=institution, register_number=register_number)
            results = student.results.select_related('exam', 'subject').all()
            
            for r in results:
                exam_name = r.exam.name if r.exam else "General Exam"
                if exam_name not in results_by_exam:
                    results_by_exam[exam_name] = {'marks': [], 'total': 0}
                results_by_exam[exam_name]['marks'].append(r)
                results_by_exam[exam_name]['total'] += r.marks
                
        except Student.DoesNotExist:
            messages.error(request, "Student not found in this institution. Please check your register number.")
    return render(request, 'student_result.html', {'form': form, 'results_by_exam': results_by_exam, 'student': student, 'institution': institution})

@login_required
def staff_dashboard_view(request):
    if not hasattr(request.user, 'institution') or not request.user.institution.is_approved:
        return redirect('results_app:pending_approval')
        
    institution = request.user.institution
    classes = Student.objects.filter(institution=institution).values_list('student_class', flat=True).distinct()
    return render(request, 'staff_dashboard.html', {'classes': sorted(list(classes))})

@login_required
def class_result_view(request, class_num):
    if not hasattr(request.user, 'institution') or not request.user.institution.is_approved:
        return redirect('results_app:pending_approval')
        
    institution = request.user.institution
    from .models import Exam
    exams = Exam.objects.filter(institution=institution).order_by('name')
    
    exam_id = request.GET.get('exam')
    selected_exam = None
    if exam_id:
        selected_exam = get_object_or_404(Exam, id=exam_id, institution=institution)
    elif exams.exists():
        selected_exam = exams.first()
        
    if selected_exam:
        students = Student.objects.filter(institution=institution, student_class=class_num).annotate(
            total_marks=Sum('results__marks', filter=models.Q(results__exam=selected_exam))
        )
    else:
        students = Student.objects.none()
        
    subjects = Subject.objects.filter(institution=institution, student_class=class_num)
    # Organize data for table
    data = []
    for s in students:
        student_results = Result.objects.filter(student=s, exam=selected_exam)
        res_dict = {r.subject.name: r.marks for r in student_results}
        
        marks_list = []
        for sub in subjects:
            marks_list.append(res_dict.get(sub.name, "-"))
            
        data.append({'student': s, 'marks': marks_list, 'total': s.total_marks or 0})
    return render(request, 'class_result.html', {'class_num': class_num, 'data': data, 'subjects': subjects, 'exams': exams, 'selected_exam': selected_exam})

@login_required
def toppers_view(request, class_num):
    if not hasattr(request.user, 'institution') or not request.user.institution.is_approved:
        return redirect('results_app:pending_approval')
        
    institution = request.user.institution
    from .models import Exam
    exams = Exam.objects.filter(institution=institution).order_by('name')
    
    exam_id = request.GET.get('exam')
    selected_exam = None
    if exam_id:
        selected_exam = get_object_or_404(Exam, id=exam_id, institution=institution)
    elif exams.exists():
        selected_exam = exams.first()
        
    if selected_exam:
        students = Student.objects.filter(institution=institution, student_class=class_num).annotate(
            total_marks=Sum('results__marks', filter=models.Q(results__exam=selected_exam))
        ).order_by('-total_marks')
    else:
        students = Student.objects.none()
        
    # Let's say top 3
    toppers = students[:3]
    return render(request, 'toppers.html', {'toppers': toppers, 'class_num': class_num, 'exams': exams, 'selected_exam': selected_exam})

@login_required
def rank_list_view(request, class_num):
    if not hasattr(request.user, 'institution') or not request.user.institution.is_approved:
        return redirect('results_app:pending_approval')
        
    institution = request.user.institution
    from .models import Exam
    exams = Exam.objects.filter(institution=institution).order_by('name')
    
    exam_id = request.GET.get('exam')
    selected_exam = None
    if exam_id:
        selected_exam = get_object_or_404(Exam, id=exam_id, institution=institution)
    elif exams.exists():
        selected_exam = exams.first()
        
    if selected_exam:
        students = Student.objects.filter(institution=institution, student_class=class_num).annotate(
            total_marks=Sum('results__marks', filter=models.Q(results__exam=selected_exam))
        ).order_by('-total_marks')
    else:
        students = Student.objects.none()
        
    return render(request, 'rank_list.html', {'students': students, 'class_num': class_num, 'exams': exams, 'selected_exam': selected_exam})

@login_required
def single_upload_view(request):
    if not hasattr(request.user, 'institution') or not request.user.institution.is_approved:
        return redirect('results_app:pending_approval')
        
    institution = request.user.institution
    if request.method == 'POST':
        form = SingleUploadForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.student.institution = institution
            result.subject.institution = institution
            # Note: Form natively validates the 'exam' foreign key belongs to the proper queryset
            result.save()
            messages.success(request, 'Result added successfully!')
            return redirect('results_app:single_upload')
    else:
        form = SingleUploadForm()
        # restrict foreign keys to the current institution
        from .models import Exam
        form.fields['student'].queryset = Student.objects.filter(institution=institution)
        form.fields['subject'].queryset = Subject.objects.filter(institution=institution)
        form.fields['exam'].queryset = Exam.objects.filter(institution=institution)
    return render(request, 'single_upload.html', {'form': form})

@login_required
def bulk_upload_view(request):
    if not hasattr(request.user, 'institution') or not request.user.institution.is_approved:
        return redirect('results_app:pending_approval')
        
    institution = request.user.institution
    
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            exam_name = form.cleaned_data['exam_name']
            
            from .models import Exam
            exam_obj, _ = Exam.objects.get_or_create(institution=institution, name=exam_name)
            
            if not (excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls')):
                messages.error(request, 'Please upload a valid Excel file (.xlsx or .xls).')
                return redirect('results_app:bulk_upload')
                
            try:
                df = pd.read_excel(excel_file)
                # Ensure all columns are treated as strings to avoid type issues
                df = df.astype(str)
                # Strip whitespace from column names
                df.columns = df.columns.str.strip()
                
                header = df.columns.tolist()
                
                if 'Register Number' not in header or 'Name' not in header or 'Class' not in header:
                    messages.error(request, 'The Excel file must contain "Register Number", "Name", and "Class" columns.')
                    return redirect('results_app:bulk_upload')
                    
                fathers_name_col = "Father's Name" if "Father's Name" in header else None
                division_col = "Division" if "Division" in header else None
                
                # Determine which columns are subjects
                fixed_cols = ['Register Number', 'Name', 'Class']
                if fathers_name_col: fixed_cols.append(fathers_name_col)
                if division_col: fixed_cols.append(division_col)
                    
                subjects = [c for c in header if c not in fixed_cols and "Unnamed" not in str(c)]
                    
                for index, row in df.iterrows():
                    reg = row['Register Number'].strip()
                    if reg == 'nan' or not reg: continue
                    
                    class_val_str = row['Class'].strip()
                    if class_val_str == 'nan' or not class_val_str: continue
                    try:
                        class_num = int(float(class_val_str))
                    except ValueError:
                        continue # Skip invalid class numbers
                    
                    name = row['Name'].strip() if str(row['Name']) != 'nan' else ''
                    fathers_name = row[fathers_name_col].strip() if fathers_name_col and str(row[fathers_name_col]) != 'nan' else None
                    division = row[division_col].strip() if division_col and str(row[division_col]) != 'nan' else None
                    
                    student, _ = Student.objects.get_or_create(
                        institution=institution,
                        register_number=reg, 
                        defaults={
                            'name': name, 
                            'student_class': class_num,
                            'fathers_name': fathers_name,
                            'division': division
                        }
                    )
                    
                    # Update fields if changed
                    updated = False
                    if fathers_name and student.fathers_name != fathers_name:
                        student.fathers_name = fathers_name
                        updated = True
                    if division and student.division != division:
                        student.division = division
                        updated = True
                    if updated:
                        student.save()
                    
                    # Update marks
                    for sub_name in subjects:
                        # Fetch / Create subject for this specific student's class
                        sub, _ = Subject.objects.get_or_create(institution=institution, name=sub_name.strip(), student_class=class_num)
                        
                        mark_val = str(row[sub_name]).strip()
                        if mark_val and mark_val != 'nan':
                            try:
                                float_mark = float(mark_val)
                                Result.objects.update_or_create(
                                    student=student,
                                    subject=sub,
                                    exam=exam_obj,
                                    defaults={'marks': float_mark}
                                )
                            except ValueError:
                                pass # Skip invalid mark values
                                
                messages.success(request, 'Bulk upload successful!')
                return redirect('results_app:staff_dashboard')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
                return redirect('results_app:bulk_upload')
                
    else:
        form = BulkUploadForm()
    return render(request, 'bulk_upload.html', {'form': form})
