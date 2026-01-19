from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    Student, AttendanceReport,
    LeaveReportStudent, FeedbackStudent,
    StudentResult, NotificationStudent
)


@login_required
def student_home(request):
    student = Student.objects.get(admin=request.user)

    attendance = AttendanceReport.objects.filter(student=student)
    present = attendance.filter(status=True).count()
    absent = attendance.filter(status=False).count()

    percentage = 0
    if present + absent > 0:
        percentage = (present / (present + absent)) * 100

    context = {
        "present": present,
        "absent": absent,
        "attendance_percentage": round(percentage, 2)
    }
    return render(request, "student_template/home_content.html", context)


@login_required
def student_view_attendance(request):
    return render(request, "student_template/student_view_attendance.html")


@login_required
def student_attendance_ajax(request):
    student = Student.objects.get(admin=request.user)
    reports = AttendanceReport.objects.filter(student=student)

    data = []
    for r in reports:
        data.append({
            "date": r.attendance.attendance_date,
            "status": "Present" if r.status else "Absent"
        })

    return JsonResponse(data, safe=False)


@login_required
def student_apply_leave(request):
    student = Student.objects.get(admin=request.user)

    if request.method == "POST":
        LeaveReportStudent.objects.create(
            student=student,
            leave_date=request.POST.get("leave_date"),
            leave_message=request.POST.get("leave_message")
        )
        messages.success(request, "Leave sent successfully")
        return redirect("student_apply_leave")

    leaves = LeaveReportStudent.objects.filter(student=student)
    return render(request, "student_template/student_apply_leave.html", {
        "leaves": leaves
    })


@login_required
def student_feedback(request):
    student = Student.objects.get(admin=request.user)

    if request.method == "POST":
        FeedbackStudent.objects.create(
            student=student,
            feedback=request.POST.get("feedback")
        )
        messages.success(request, "Feedback sent")
        return redirect("student_feedback")

    feedbacks = FeedbackStudent.objects.filter(student=student)
    return render(request, "student_template/student_feedback.html", {
        "feedbacks": feedbacks
    })


@login_required
def student_profile(request):
    student = Student.objects.get(admin=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.save()

        student.address = request.POST.get("address")
        student.gender = request.POST.get("gender")

        if "profile_pic" in request.FILES:
            student.profile_pic = request.FILES["profile_pic"]

        student.save()
        messages.success(request, "Profile updated")
        return redirect("student_profile")

    return render(request, "student_template/student_view_profile.html", {
        "student": student
    })


@login_required
def student_view_result(request):
    student = Student.objects.get(admin=request.user)
    results = StudentResult.objects.filter(student=student)

    return render(request, "student_template/student_view_result.html", {
        "results": results
    })


@login_required
def student_notifications(request):
    student = Student.objects.get(admin=request.user)
    notifications = NotificationStudent.objects.filter(student=student)
    return render(request, "student_template/student_view_notification.html", {
        "notifications": notifications
    })
