from django.urls import path

from config.urls import urlpatterns
from . import staff_views, student_views

urlpatterns = [
    path('staff_apply_leave/', staff_views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_feedback/', staff_views.staff_feedback, name="staff_feedback"),
    path('staff_all_notification/', staff_views.staff_all_notification, name="staff_all_notification"),

    path('student_all_notification/', student_views.student_all_notification, name="student_all_notification")
]
