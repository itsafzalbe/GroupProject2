from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import Staff, LeaveReportStaff, FeedbackStaff, NotificationStaff


# STAFF APPLY LEAVE

def staff_apply_leave(request):
    """
    Xodim ta'til uchun ariza yuborishi
    """
    staff_obj = get_object_or_404(Staff, admin=request.user)
    leave_history = LeaveReportStaff.objects.filter(staff=staff_obj).order_by('-created_at')

    if request.method == "POST":
        date = request.POST.get('leave_date')
        message = request.POST.get('leave_message')

        try:
            leave = LeaveReportStaff(staff=staff_obj, date=date, message=message, status=0)
            leave.save()
            messages.success(request, "Ta'til arizasi yuborildi.")
            return redirect('staff_apply_leave')
        except Exception:
            messages.error(request, "Xatolik yuz berdi!")

    context = {
        "leave_history": leave_history,
        "page_title": "Apply Leave"
    }
    return render(request, "staff_template/staff_apply_leave.html", context)



# STAFF FEEDBACK

def staff_feedback(request):
    """
    Xodim fikr-mulohaza yuborishi va javoblarni ko'rishi
    """
    staff_obj = get_object_or_404(Staff, admin=request.user)
    feedback_history = FeedbackStaff.objects.filter(staff=staff_obj).order_by('-created_at')

    if request.method == "POST":
        feedback = request.POST.get('feedback_msg')
        try:
            add_feedback = FeedbackStaff(staff=staff_obj, feedback=feedback, reply="")
            add_feedback.save()
            messages.success(request, "Fikr-mulohaza yuborildi.")
            return redirect('staff_feedback')
        except Exception:
            messages.error(request, "Xatolik yuz berdi!")

    context = {
        "feedback_history": feedback_history,
        "page_title": "Staff Feedback"
    }
    return render(request, "staff_template/staff_feedback.html", context)



# STAFF NOTIFICATIONS

def staff_view_notification(request):
    """
    Xodimga kelgan bildirishnomalarni ko'rsatish
    """
    staff_obj = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff_obj).order_by('-created_at')

    context = {
        "notifications": notifications,
        "page_title": "View Notifications"
    }
    return render(request, "staff_template/staff_view_notification.html", context)
