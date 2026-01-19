from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Staff, LeaveReportStaff, FeedbackStaff, NotificationStaff


def staff_apply_leave(request):
    """Xodim ta'til uchun ariza yuborishi"""

    staff_obj = Staff.objects.get(admin=request.user)
    leave_data = LeaveReportStaff.objects.filter(staff=staff_obj)

    if request.method == "POST":
        date = request.POST.get('leave_date')
        message = request.POST.get('leave_message')

        try:
            leave = LeaveReportStaff(staff=staff_obj, date=date, message=message, status=0)
            leave.save()
            messages.success(request, "Ta'til arizasi yuborildi.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Xatolik yuz berdi!")

    return render(request, "staff_template/staff_apply_leave.html", {"leave_data": leave_data})


def staff_feedback(request):
    """Xodim fikr-mulohaza yuborishi va javoblarni ko'rishi"""

    staff_obj = Staff.objects.get(admin=request.user)
    feedback_data = FeedbackStaff.objects.filter(staff=staff_obj)

    if request.method == "POST":
        feedback = request.POST.get('feedback_msg')
        try:
            add_feedback = FeedbackStaff(staff=staff_obj, feedback=feedback, reply="")
            add_feedback.save()
            messages.success(request, "Fikr-mulohaza yuborildi.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Xatolik yuz berdi!")

    return render(request, "staff_template/staff_feedback.html", {"feedback_data": feedback_data})


def staff_all_notification(request):
    """Xodimga kelgan bildirishnomalarni ko'rsatish"""

    staff_obj = Staff.objects.get(admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff_obj)
    return render(request, "staff_template/all_notification.html", {"notifications": notifications})