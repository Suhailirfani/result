import os
import django
from django.contrib.auth.models import User
from results_app.models import Institution, Student, Subject, Exam, Result
import random

def populate():
    # Create Institution 1 (10-Point CBSE)
    user1, _ = User.objects.get_or_create(username='cbse_school', defaults={'email': 'cbse@test.com'})
    user1.set_password('password123')
    user1.save()
    
    inst1, _ = Institution.objects.get_or_create(
        user=user1,
        defaults={
            'name': 'Delhi Public School (Dummy)',
            'phone_number': '1234567890',
            'is_approved': True,
            'grading_system': '10_POINT'
        }
    )
    inst1.is_approved = True
    inst1.save()

    # Create Institution 2 (9-Point Kerala)
    user2, _ = User.objects.get_or_create(username='kerala_school', defaults={'email': 'kerala@test.com'})
    user2.set_password('password123')
    user2.save()

    inst2, _ = Institution.objects.get_or_create(
        user=user2,
        defaults={
            'name': 'Govt Higher Secondary (Dummy)',
            'phone_number': '0987654321',
            'is_approved': True,
            'grading_system': '9_POINT'
        }
    )
    inst2.is_approved = True
    inst2.save()

    print("Created Institutions: 'cbse_school' and 'kerala_school' (Password: password123)")

    for inst in [inst1, inst2]:
        # Exam
        exam, _ = Exam.objects.get_or_create(institution=inst, name='Final Examination 2026')
        
        # Subjects for Class 10
        subjects_names = ['English', 'Mathematics', 'Science', 'Social Science', 'Second Language']
        subjects = []
        for sname in subjects_names:
            sub, _ = Subject.objects.get_or_create(institution=inst, name=sname, student_class=10)
            subjects.append(sub)

        # Students
        students_data = [
            ('Alice Smith', 'A'),
            ('Bob Johnson', 'A'),
            ('Charlie Brown', 'B'),
            ('Diana Prince', 'B'),
            ('Evan Wright', 'C'),
        ]
        
        for i, (name, div) in enumerate(students_data):
            reg_no = f"REG{inst.id}00{i+1}"
            student, _ = Student.objects.get_or_create(
                institution=inst,
                register_number=reg_no,
                defaults={
                    'name': name,
                    'fathers_name': f"Father of {name}",
                    'student_class': 10,
                    'division': div
                }
            )
            
            # Create Results
            for sub in subjects:
                # Give random marks between 30 and 100
                Result.objects.update_or_create(
                    student=student,
                    subject=sub,
                    exam=exam,
                    defaults={'marks': float(random.randint(30, 100))}
                )
    print("Database populated successfully with dummy data!")

if __name__ == '__main__':
    populate()
