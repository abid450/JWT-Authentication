from django.db.models import Count, Q, Window, F
from django.db.models.functions import DenseRank
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.functions import TruncMonth

from .models import *

# Attendance Summary ---------------------------------
def update_attendance_summary(student):
    qs = student.attendances.aggregate(
        total_days=Count('id'),
        present_days=Count('id', filter=Q(status='Present')),
        absent_days=Count('id', filter=Q(status='Absent')),
        late_days=Count('id', filter=Q(status='Late')),
    )

    summary, _ = AttendanceSummary.objects.get_or_create(
        student=student,
        defaults={'roll': student.roll}
    )

    summary.roll = student.roll
    summary.total_days = qs['total_days']
    summary.present_days = qs['present_days']
    summary.absent_days = qs['absent_days']
    summary.late_days = qs['late_days']
    summary.total_present_days = qs['present_days']
    summary.save()


def update_ranking():
    summaries = AttendanceSummary.objects.annotate(
        rank_calc=Window(
            expression=DenseRank(),
            order_by=F('total_present_days').desc()
        )
    )

    for s in summaries:
        s.rank = s.rank_calc
        s.save(update_fields=['rank'])



# Attendence RankSummary ---------------------------------------------
def build_attendance_rank_summary():
    AttendanceRankSummary.objects.all().delete()

    summaries = AttendanceSummary.objects.select_related(
        'student', 'student__Section'
    )

    for s in summaries:
        AttendanceRankSummary.objects.create(
            student=s.student,
            student_name=s.student.name,
            roll=s.student.roll,
            class_name=s.student.Class_name,
            section=s.student.Section.name,
            total_present=s.total_present_days,
            rank=s.rank
        )


# Monthly Attendence Report --------------------------------------
def generate_monthly_reports():
    monthly_data = (
        Attendance.objects
        .annotate(month=TruncMonth('date'))   # ✅ auto year+month
        .values('student_id', 'month')
        .annotate(
            total_days=Count('id'),
            present_days=Count('id', filter=Q(status='Present')),
            absent_days=Count('id', filter=Q(status='Absent')),
            late_days=Count('id', filter=Q(status='Late')),
        )
    )

    for row in monthly_data:
        AttendanceMonthlyReport.objects.update_or_create(
            student_id=row['student_id'],
            month=row['month'],  # 🔥 2026-01-01
            defaults={
                'total_days': row['total_days'],
                'present_days': row['present_days'],
                'absent_days': row['absent_days'],
                'late_days': row['late_days'],
                'total_present_days': row['present_days'],
            }
        )