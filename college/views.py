from rest_framework.viewsets import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, F, Window, Q, When, Value, CharField, Case
from django.db.models.functions import DenseRank
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from datetime import *
from django.db.models import (
    Q, F, FloatField, ExpressionWrapper, Case, When, Value
)

import calendar


# Student Viewset -----------------------------------
class StudentView(ModelViewSet):
    queryset = Student.objects.all().select_related('classroom').prefetch_related('marks')
    serializer_class = Student_info
    permission_classes = [AllowAny]


    def get_queryset(self):
        qs = super().get_queryset().annotate(
            total_marks = Sum('marks__marks_obtained'),
            avg_marks = Avg('marks__marks_obtained')
        )

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(roll__icontains=search))
        
        return qs
    

# Pagination ------------------------------------------------------
class MarkResulPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50



# Mark View ---------------------------------------------------
class MarkViewSet(ModelViewSet):
    queryset = Student.objects.prefetch_related('marks__subject', 'marks__exam').all()
    serializer_class = StudentWithMarksSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']
    pagination_class = MarkResulPagination

    def get_queryset(self):
        qs = self.queryset

        # Multiple search: student name or roll
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(roll__icontains=search))

        # Filter by exam
        exam = self.request.query_params.get('exam')
        if exam:
            qs = qs.filter(marks__exam__name__icontains=exam)

        # Filter by subject
        subject = self.request.query_params.get('subject')
        if subject:
            qs = qs.filter(marks__subject__name__icontains=subject)

        # Annotate total, avg, rank
        qs = qs.annotate(
            total_student_marks=Sum('marks__marks_obtained'),
            avg_student_marks=Avg('marks__marks_obtained'),
            rank=Window(
                expression=DenseRank(),
                order_by=Avg('marks__marks_obtained').desc()
            )
        ).distinct()

        return qs


# Attendence --------------------------------------------------
class AttendanceCreateViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']



# Attendence Summary---------------------------------------------
class AttendanceViewSet(ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        params = self.request.query_params

        base_qs = Attendance.objects.select_related(
            'student', 'student__Section'
        )

        search = params.get('search')
        if search:
            base_qs = base_qs.filter(
                Q(student__name__icontains=search) |
                Q(student__roll__icontains=search)
            )

        # filter ------------------------
        class_name = params.get('class')
        if class_name:
            qs = qs.filter(student__Class_name=class_name)


        qs = base_qs.values(
            'student_id',
            student_name=F('student__name'),
            roll=F('student__roll'),
            Class_name=F('student__Class_name'),
            Section=F('student__Section__name'),

        ).annotate(
            total_days=Count('id'),
            present_days=Count('id', filter=Q(status='Present')),
            absent_days=Count('id', filter=Q(status='Absent')),
            late_days=Count('id', filter=Q(status='Late')),
            total_present_days=Count('id', filter=Q(status='Present')),
            
            # Rank ----
            rank=Window(
                expression=DenseRank(),
                order_by=F('total_present_days').desc()
            )
        )

        return qs


# Monthly Attendance Report --------------------------------------

# pagination ----------------
class MonthlyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# Monthly Wise Attendance Report --------------------------------------------------
class AttendanceMonthlyReportView(ModelViewSet):
    serializer_class = AttendanceMonthlyReportSerializer
    permission_classes = [AllowAny]
    pagination_class = MonthlyPagination
    http_method_names = ['get']

    def get_queryset(self):
        qs = AttendanceMonthlyReport.objects.select_related(
            'student',
            'student__Section'
        ).filter(total_days__gt=0)

        params = self.request.query_params

        search = params.get('search')
        if search:
            qs = qs.filter(
                Q(student__name__icontains=search) |
                Q(student__roll__icontains=search)
            )
            
        # filter --------------------------
        month_name = params.get('month_name')
        if month_name:
            qs = qs.filter(month_name__icontains=month_name)

        class_name = params.get('class')
        if class_name:
            qs = qs.filter(student__Class_name=class_name)

        return qs.annotate(
            attendance_percentage=ExpressionWrapper(
                (F('total_present_days') * 100.0) / F('total_days'),
                output_field=FloatField()
            )
        ).order_by('student__roll')
