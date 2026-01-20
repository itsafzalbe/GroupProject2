from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json, math

from .models import (
    Student, NotificationStudent, LeaveReportStudent,
    FeedbackStudent, Attendance, AttendanceReport, Subject, Course, StudentResult
)

# -----------------------------
# STUDENT HOME
# -----------------------------
def student_home(request):
    student = get_object_or_404(Student, admin=request.user)
    subjects = Subject.objects.filter(course=student.course)
    total_subject = subjects.count()
    total_attendance = AttendanceReport.objects.filter(student=student).count()
    total_present = AttendanceReport.objects.filter(student=student, status=True).count()

    if total_attendance == 0:
        percent_present = percent_absent = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = 100 - percent_present

    subject_name = []
    data_present = []
    data_absent = []
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, student=student, status=True
        ).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, student=student, status=False
        ).count()
        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)

    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': 'Student Home'
    }
    return render(request, "student_template/home_content.html", context)

# -----------------------------
# STUDENT APPLY LEAVE
# -----------------------------
def student_apply_leave(request):
    student = get_object_or_404(Student, admin=request.user)
    leave_history = LeaveReportStudent.objects.filter(student=student).order_by('-created_at')

    if request.method == "POST":
        date = request.POST.get('leave_date')
        message = request.POST.get('leave_message')
        try:
            leave = LeaveReportStudent(student=student, date=date, message=message, status=0)
            leave.save()
            messages.success(request, "Ta'til arizasi yuborildi.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Xatolik yuz berdi!")

    context = {
        "leave_history": leave_history,
        "page_title": "Apply Leave"
    }
    return render(request, "student_template/student_apply_leave.html", context)

# -----------------------------
# STUDENT FEEDBACK
# -----------------------------
def student_feedback(request):
    student = get_object_or_404(Student, admin=request.user)
    feedback_history = FeedbackStudent.objects.filter(student=student).order_by('-created_at')

    if request.method == "POST":
        feedback = request.POST.get('feedback_msg')
        try:
            add_feedback = FeedbackStudent(student=student, feedback=feedback, reply="")
            add_feedback.save()
            messages.success(request, "Fikr-mulohaza yuborildi.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Xatolik yuz berdi!")

    context = {
        "feedback_history": feedback_history,
        "page_title": "Student Feedback"
    }
    return render(request, "student_template/student_feedback.html", context)

# -----------------------------
# STUDENT VIEW NOTIFICATIONS
# -----------------------------
def student_view_notification(request):
    student = get_object_or_404(Student, admin=request.user)
    notifications = NotificationStudent.objects.filter(student=student).order_by('-created_at')

    context = {
        "notifications": notifications,
        "page_title": "View Notifications"
    }
    return render(request, "student_template/student_view_notification.html", context)

# -----------------------------
# STUDENT VIEW ATTENDANCE
# -----------------------------
@csrf_exempt
def student_view_attendance(request):
    student = get_object_or_404(Student, admin=request.user)

    if request.method != 'POST':
        context = {
            'subjects': Subject.objects.filter(course=student.course),
            'page_title': 'View Attendance'
        }
        return render(request, "student_template/student_view_attendance.html", context)
    else:
        subject_id = request.POST.get('subject')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(attendance__in=attendance, student=student)
            data = [{"date": str(r.attendance.date), "status": r.status} for r in attendance_reports]
            return JsonResponse(data, safe=False)
        except Exception:
            return JsonResponse([], safe=False)

# -----------------------------
# STUDENT VIEW RESULT
# -----------------------------
def student_view_result(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('-created_at')
    context = {
        'results': results,
        'page_title': 'View Results'
    }
    return render(request, "student_template/student_view_result.html", context)
