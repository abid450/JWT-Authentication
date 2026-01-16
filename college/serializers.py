from rest_framework import serializers
from .models import *
from django.db.models import Sum, Avg



class Student_info(serializers.ModelSerializer):
    total_marks = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    avg_marks = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'Class_name',  'Section', 'total_marks', 'avg_marks']



# Nested serializer for each subject's mark
class MarkNestedSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    Exam_name = serializers.CharField(source='exam.name', read_only=True)
    Out_of = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    percentage = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    class Meta:
        model = Mark
        fields = ['subject_name', 'marks_obtained', 'Out_of', 'Exam_name', 'percentage', 'grade']

    def get_percentage(self, obj):
        return round(float(obj.marks_obtained * 100 / obj.Out_of), 2)

    def get_grade(self, obj):
        pct = float(obj.marks_obtained * 100 / obj.Out_of)
        if pct >= 80:
            return "A+"
        elif pct >= 70:
            return "A"
        elif pct >= 60:
            return "A-"
        elif pct >= 50:
            return "B"
        elif pct >= 40:
            return "C"
        elif pct >= 33:
            return "D"
        return "F"



# Main serializer for student with aggregated data
class StudentWithMarksSerializer(serializers.ModelSerializer):
    subjects = MarkNestedSerializer(source='marks', many=True)
    total_student_marks = serializers.SerializerMethodField()
    avg_student_marks = serializers.SerializerMethodField()
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'subjects', 'total_student_marks', 'avg_student_marks', 'rank']

    def get_total_student_marks(self, obj):
        return float(obj.marks.aggregate(total=Sum('marks_obtained'))['total'] or 0)

    def get_avg_student_marks(self, obj):
        return round(float(obj.marks.aggregate(avg=Avg('marks_obtained'))['avg'] or 0), 2)
    


class RankingSerializer(serializers.ModelSerializer):
    total_marks = serializers.DecimalField(max_digits=10, decimal_places=2)
    rank = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ['name', 'roll', 'total_marks', 'rank']


# Attendence ---------------------------------
class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'remarks']



# Attendence Summary ---------------------------------------------
class AttendanceSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    roll = serializers.IntegerField()
    Section = serializers.CharField()
    Class_name = serializers.CharField()
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    total_present_days = serializers.IntegerField()
    rank = serializers.IntegerField()


    class Meta:
        model = Attendance
        fields = [
            'student_id',
            'student_name',
            'roll',
            'Section',
            'Class_name',
            'total_days',
            'present_days',
            'absent_days',
            'late_days',
            'total_present_days',
            'rank'
        ]

    def get_total_days(self, obj):
        return obj.student.attendances.count()
        
    
    # ✅ Present দিন
    def get_present_days(self, obj):
        return obj.student.attendances.filter(status='Present').count()

    # ✅ Absent দিন
    def get_absent_days(self, obj):
        return obj.student.attendances.filter(status='Absent').count()

    # ✅ Late দিন
    def get_late_days(self, obj):
        return obj.student.attendances.filter(status='Late').count()




class AttendanceMonthlyReportSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    roll = serializers.IntegerField(source='student.roll', read_only=True)
    class_name = serializers.CharField(source='student.Class_name', read_only=True)
    section = serializers.CharField(source='student.Section.name', read_only=True)
    month_name = serializers.SerializerMethodField()
    attendance_percentage = serializers.FloatField(read_only=True)  

    
    class Meta:
        model = AttendanceMonthlyReport
        fields = [
            'student_name', 
            'roll', 
            'class_name', 
            'section', 
            'month_name',
            'total_days',
            'present_days', 
            'absent_days', 
            'late_days', 
            'total_present_days', 
            'attendance_percentage'

        ]

    
    def get_month_name(self, obj):
        return obj.month.strftime('%B %Y')  # 🔥 January 2026


