from college.models import *

class AttendanceAlertService:

    @staticmethod
    def get_all_status(queryset=None):
       
        if queryset is None:
            queryset = AttendanceMonthlyReport.objects.select_related('student', 'student__Section')

        result = []

        for student in queryset:
            total_days = student.total_days or 0
            present_days = student.total_present_days or 0

            if total_days > 0:
                percentage = (present_days / total_days) * 100
            else:
                percentage = 0.0

            # Determine status
            if percentage < 50:
                status = "Critical"

            elif percentage < 75:
                status = "Warning"
                
            else:
                status = "Safe"

            result.append({
                "student_name": student.student.name,
                "roll": student.student.roll,
                "class_name": student.student.Class_name,
                "section": student.student.Section.name,
                "total_days": total_days,
                "present_days": present_days,
                "attendance_percentage": round(percentage, 2),
                "status": status
            })
        return result
