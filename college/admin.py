from django.contrib import admin
from .models import *
from django.db.models import F, ExpressionWrapper, FloatField

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(ClassRoom)
admin.site.register(Exam)
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'student', 'exam', 'subject', 'marks_obtained', 'Out_of']
    
    search_fields = (
        'student__name',
        'student__roll'
        
    )

    list_filter = ['id', 'student']


@admin.register(Attendance)
class attendanceAdmin(admin.ModelAdmin):
    list_filter = ['student']


@admin.register(AttendanceSummary)
class AttendenceAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'roll',
        'total_days',
        'present_days', 
        'absent_days', 
        'late_days', 
        'total_present_days', 
        'rank',
        'updated_at',
        )

    search_fields = (
                    'student__name',
                    'student__roll',
                     )

    list_filter = ['rank']





@admin.register(AttendanceRankSummary)
class AttendanceRankSummaryAdmin(admin.ModelAdmin):
    list_display = (
        'rank',
        'student_name',
        'roll',
        'class_name',
        'section',
        'total_present',
    )

    list_filter = ('rank', 'class_name', 'section')
    search_fields = ('student_name', 'roll')
    ordering = ('rank',)



@admin.register(AttendanceMonthlyReport)
class AttendanceMonthlyReportAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'student_roll',
        'student_class',
        'student_section',
        'month',
        'total_days',
        'present_days',
        'absent_days',
        'late_days',
        'total_present_days',
        'attendance_percentage_display',
    )

    list_select_related = ('student', 'student__Section')

    list_filter = (
        'month',
        'student__Class_name',
        'student__Section',
    )

    search_fields = (
        'student__name',
        'student__roll',
    )

    ordering = ('-month', 'student__roll')

    readonly_fields = (
        'total_days',
        'present_days',
        'absent_days',
        'late_days',
        'total_present_days',
    )

    # 🔹 Extra annotations for admin list page
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(total_days__gt=0).annotate(
            attendance_percentage=ExpressionWrapper(
                (F('total_present_days') * 100.0) / F('total_days'),
                output_field=FloatField()
            )
        )

    # -------------------------
    # Custom display methods
    # -------------------------

    def student_roll(self, obj):
        return obj.student.roll
    student_roll.short_description = "Roll"

    def student_class(self, obj):
        return obj.student.Class_name
    student_class.short_description = "Class"

    def student_section(self, obj):
        return obj.student.Section.name if obj.student.Section else "-"
    student_section.short_description = "Section"

    def month(self, obj):
        return obj.month.strftime("%B %Y")
    month.short_description = "Month"

    def attendance_percentage_display(self, obj):
        return f"{round(obj.attendance_percentage, 2)} %"
    attendance_percentage_display.short_description = "Attendance_Percentage"