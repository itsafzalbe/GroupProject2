from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import (
    Staff, Student, Subject, Session,
    LeaveReportStaff, FeedbackStaff, NotificationStaff
)


def staff_dashboard(request):
    staff = get_object_or_404(Staff, admin=request.user)

    students_count = Student.objects.filter(course=staff.course).count()
    subjects_count = Subject.objects.filter(staff=staff).count()
    leave_count = LeaveReportStaff.objects.filter(staff=staff).count()

    context = {
        "page_title": "Staff Dashboard",
        "students_count": students_count,
        "subjects_count": subjects_count,
        "leave_count": leave_count
    }
    return render(request, "staff_template/home_content.html", context)


def staff_leave_request(request):
    staff = get_object_or_404(Staff, admin=request.user)
    leave_history = LeaveReportStaff.objects.filter(staff=staff)

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        reason = request.POST.get("leave_message")

        if leave_date and reason:
            LeaveReportStaff.objects.create(
                staff=staff,
                date=leave_date,
                message=reason,
                status=0
            )
            messages.success(request, "Ta'til arizasi yuborildi")
            return redirect("staff_leave_request")
        else:
            messages.error(request, "Barcha maydonlarni to‘ldiring")

    return render(request, "staff_template/staff_apply_leave.html", {
        "leave_history": leave_history,
        "page_title": "Apply Leave"
    })


def staff_send_feedback(request):
    staff = get_object_or_404(Staff, admin=request.user)
    feedbacks = FeedbackStaff.objects.filter(staff=staff)

    if request.method == "POST":
        msg = request.POST.get("feedback_msg")

        if msg:
            FeedbackStaff.objects.create(
                staff=staff,
                feedback=msg,
                reply=""
            )
            messages.success(request, "Feedback yuborildi")
            return redirect("staff_send_feedback")
        else:
            messages.error(request, "Feedback bo‘sh bo‘lmasin")

    return render(request, "staff_template/staff_feedback.html", {
        "feedback_history": feedbacks,
        "page_title": "Staff Feedback"
    })


def staff_notifications(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)

    return render(request, "staff_template/staff_view_notification.html", {
        "notifications": notifications,
        "page_title": "Notifications"
    })


def staff_profile_view(request):
    staff = get_object_or_404(Staff, admin=request.user)
    admin = staff.admin

    if request.method == "POST":
        admin.first_name = request.POST.get("first_name")
        admin.last_name = request.POST.get("last_name")

        if request.FILES.get("profile_pic"):
            fs = FileSystemStorage()
            file = fs.save(request.FILES["profile_pic"].name, request.FILES["profile_pic"])
            admin.profile_pic = fs.url(file)

        admin.save()
        messages.success(request, "Profil yangilandi")
        return redirect("staff_profile_view")

    return render(request, "staff_template/staff_view_profile.html", {
        "staff": staff,
        "page_title": "My Profile"
    })
