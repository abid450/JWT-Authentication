from .models import *
from .service import *



@receiver(post_save, sender=Attendance)
@receiver(post_delete, sender=Attendance)
def attendance_changed(sender, instance, **kwargs):
    update_attendance_summary(instance.student)
    update_ranking()
    build_attendance_rank_summary()
    generate_monthly_reports()
