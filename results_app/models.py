from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution')
    name = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Approved' if self.is_approved else 'Pending'})"

class Student(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255, blank=True, null=True)
    register_number = models.CharField(max_length=50, db_index=True)
    student_class = models.IntegerField()  # 1 to 10
    division = models.CharField(max_length=10, blank=True, null=True) # e.g. 'A', 'B'
    
    class Meta:
        unique_together = ('institution', 'register_number')

    def __str__(self):
        div_str = f" {self.division}" if self.division else ""
        return f"{self.name} ({self.register_number}) - Class {self.student_class}{div_str}"

class Subject(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    student_class = models.IntegerField()

    class Meta:
        unique_together = ('institution', 'name', 'student_class')

    def __str__(self):
        return f"{self.name} (Class {self.student_class})"

class Exam(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('institution', 'name')

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', null=True)
    marks = models.FloatField()

    class Meta:
        unique_together = ('student', 'subject', 'exam')

    def __str__(self):
        exam_name = self.exam.name if self.exam else "Unassigned"
        return f"{self.student.name} - {self.subject.name} ({exam_name}): {self.marks}"
