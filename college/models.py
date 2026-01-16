from django.db import models
from django.utils import timezone

# Create your models here.
from django.shortcuts import render
from django.db import models
from django.db.models import Q
# Create your views here.

class StudentQueryset(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def search(self, keyword):
        return self.filter(
            Q(name__icontains=keyword) | Q(roll__icontains=keyword)

        )
    
# Student Manager ---------------------------------
class StudentManager(models.Manager):
    def get_queryset(self):
        return StudentQueryset(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    

# Section ------------------------------------------------
class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.year})"


# Student -------------------------------------------------
class Student(models.Model):
    class_choices = {
        ('Class 6', 'Class 6'),
        ('Class 7', 'Class 7'),
        ('Class 8', 'Class 8'),
        ('Class 9', 'Class 9'),
        ('Class 10', 'Class 10'),

    }

    name = models.CharField(max_length=150)
    roll = models.IntegerField(unique=True)
    Class_name = models.CharField(max_length=50, choices=class_choices)
    Section = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    is_active = models.BooleanField(default=True)

    objects = StudentManager()

    def __str__(self):
        return self.name
    


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Exam(models.Model):
    exam_name ={
        ('Mid Term', 'Mid Term'),
        ('Test Exam', 'Test Exam'),
        ('Final Exam', 'Final Exam')
    }
    
    name = models.CharField(choices=exam_name, max_length=50)
    date = models.DateField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='exams')

    def __str__(self):
        return f"{self.name} - {self.classroom.name}"
    


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    Out_of = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    

    class Meta:
        unique_together = ('student', 'exam', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.marks_obtained}"


class MarkSummary(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name='mark_summary')
    roll = models.IntegerField()
    

# Attendance ------------------------------------
class Attendance(models.Model):
    Attendance_Status = {
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        
    }

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Attendance_Status)
    remarks = models.TextField(blank=True, null=True)


    @property
    def roll(self):
        return self.student.roll


    class Meta:
        unique_together = ('student', 'date')  # এক student এক দিন একবার attendance

   
    def __str__(self):
        return f"{self.student.name} - {self.roll} - {self.status}"
    

# Attendence Summury ----------------------------------------------------
class AttendanceSummary(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_summary'
    )
    roll = models.IntegerField()
    total_days = models.PositiveIntegerField(default=0)
    present_days = models.PositiveIntegerField(default=0)
    absent_days = models.PositiveIntegerField(default=0)
    late_days = models.PositiveIntegerField(default=0)

    total_present_days = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance Summary"


# Attendance Rank Summary -------------------------------------------------
class AttendanceRankSummary(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_rank'
    )

    student_name = models.CharField(max_length=150)
    roll = models.IntegerField()
    section = models.CharField(max_length=50)
    class_name = models.CharField(max_length=50)

    total_present = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance Rank Summary"
        

    def __str__(self):
        return f"{self.student_name} | Rank {self.rank}"




class AttendanceMonthlyReport(models.Model):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
     
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='monthly_reports')
    month = models.DateField()
    total_days = models.PositiveIntegerField(default=0)
    present_days = models.PositiveIntegerField(default=0)
    absent_days = models.PositiveIntegerField(default=0)
    late_days = models.PositiveIntegerField(default=0)
    total_present_days = models.PositiveIntegerField(default=0)  # extra field
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('student', 'month')
        ordering = ['-month']



    def __str__(self):
        return f"{self.student.name} | {self.month}"
    
