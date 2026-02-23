from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Subject, Result
from .forms import StudentSearchForm, SingleUploadForm, BulkUploadForm
from django.db.models import Sum
import pandas as pd

def home_view(request):
    return render(request, 'home.html')

def student_result_view(request):
    form = StudentSearchForm(request.GET or None)
    results = None
    student = None
    total_marks = 0
    if request.GET and form.is_valid():
        register_number = form.cleaned_data['register_number']
        try:
            student = Student.objects.get(register_number=register_number)
            results = student.results.all()
            total_marks = sum(r.marks for r in results)
        except Student.DoesNotExist:
            messages.error(request, "Student not found. Please check your name and register number.")
    return render(request, 'student_result.html', {'form': form, 'results': results, 'student': student, 'total_marks': total_marks})

@login_required
def staff_dashboard_view(request):
    # Classes available
    classes = Student.objects.values_list('student_class', flat=True).distinct()
    return render(request, 'staff_dashboard.html', {'classes': sorted(list(classes))})

@login_required
def class_result_view(request, class_num):
    students = Student.objects.filter(student_class=class_num).annotate(total_marks=Sum('results__marks'))
    subjects = Subject.objects.filter(student_class=class_num)
    # Organize data for table
    data = []
    for s in students:
        student_results = Result.objects.filter(student=s)
        res_dict = {r.subject.name: r.marks for r in student_results}
        
        marks_list = []
        for sub in subjects:
            marks_list.append(res_dict.get(sub.name, "-"))
            
        data.append({'student': s, 'marks': marks_list, 'total': s.total_marks or 0})
    return render(request, 'class_result.html', {'class_num': class_num, 'data': data, 'subjects': subjects})

@login_required
def toppers_view(request, class_num):
    students = Student.objects.filter(student_class=class_num).annotate(total_marks=Sum('results__marks')).order_by('-total_marks')
    # Let's say top 3
    toppers = students[:3]
    return render(request, 'toppers.html', {'toppers': toppers, 'class_num': class_num})

@login_required
def rank_list_view(request, class_num):
    students = Student.objects.filter(student_class=class_num).annotate(total_marks=Sum('results__marks')).order_by('-total_marks')
    return render(request, 'rank_list.html', {'students': students, 'class_num': class_num})

@login_required
def single_upload_view(request):
    if request.method == 'POST':
        form = SingleUploadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully!')
            return redirect('results_app:single_upload')
    else:
        form = SingleUploadForm()
    return render(request, 'single_upload.html', {'form': form})

@login_required
def bulk_upload_view(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            class_num = form.cleaned_data['student_class']
            
            if not (excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls')):
                messages.error(request, 'Please upload a valid Excel file (.xlsx or .xls).')
                return redirect('results_app:bulk_upload')
                
            try:
                df = pd.read_excel(excel_file)
                # Ensure all columns are treated as strings to avoid type issues with registers/names
                df = df.astype(str)
                # Strip whitespace from column names
                df.columns = df.columns.str.strip()
                
                header = df.columns.tolist()
                
                if 'Register Number' not in header or 'Name' not in header:
                    messages.error(request, 'The Excel file must contain "Register Number" and "Name" columns.')
                    return redirect('results_app:bulk_upload')
                    
                fathers_name_col = "Father's Name" if "Father's Name" in header else None
                
                # Determine which columns are subjects
                fixed_cols = ['Register Number', 'Name']
                if fathers_name_col:
                    fixed_cols.append(fathers_name_col)
                    
                subjects = [c for c in header if c not in fixed_cols and "Unnamed" not in str(c)]
                
                # Fetch / Create subjects for this class
                subject_objs = {}
                for sub_name in subjects:
                    sub, _ = Subject.objects.get_or_create(name=sub_name.strip(), student_class=class_num)
                    subject_objs[sub_name] = sub
                    
                for index, row in df.iterrows():
                    reg = row['Register Number'].strip()
                    if reg == 'nan' or not reg: continue
                    
                    name = row['Name'].strip() if str(row['Name']) != 'nan' else ''
                    fathers_name = row[fathers_name_col].strip() if fathers_name_col and str(row[fathers_name_col]) != 'nan' else None
                    
                    student, _ = Student.objects.get_or_create(
                        register_number=reg, 
                        defaults={
                            'name': name, 
                            'student_class': class_num,
                            'fathers_name': fathers_name
                        }
                    )
                    
                    # If student exists but fathers name is new, update it
                    if fathers_name and student.fathers_name != fathers_name:
                        student.fathers_name = fathers_name
                        student.save()
                    
                    # Update marks
                    for sub_name in subjects:
                        mark_val = str(row[sub_name]).strip()
                        if mark_val and mark_val != 'nan':
                            try:
                                float_mark = float(mark_val)
                                Result.objects.update_or_create(
                                    student=student,
                                    subject=subject_objs[sub_name],
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
