from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255, blank=True, null=True)
    register_number = models.CharField(max_length=50, unique=True, db_index=True)
    student_class = models.IntegerField()  # 1 to 10

    def __str__(self):
        return f"{self.name} ({self.register_number}) - Class {self.student_class}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    student_class = models.IntegerField()

    class Meta:
        unique_together = ('name', 'student_class')

    def __str__(self):
        return f"{self.name} (Class {self.student_class})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    marks = models.FloatField()

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks}"
