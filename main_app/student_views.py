from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json, math

from .forms import StudentEditForm
from .models import (
    Student, NotificationStudent, LeaveReportStudent,
    FeedbackStudent, Attendance, AttendanceReport, Subject, Course, StudentResult, CustomUser
)


# student home
# student apply leave
# student feedback
# student view notification <- this is not needed, anything related to notifications
# student view attendance
# stuednt view result


# Qilinishi kerak

# student view profile
# student fcm token


def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(
        request.POST or None,
        request.FILES or None,
        instance=student
    )

    if request.method == 'POST':
        if form.is_valid():
            admin = student.admin
            admin.first_name = form.cleaned_data.get('first_name')
            admin.last_name = form.cleaned_data.get('last_name')
            admin.address = form.cleaned_data.get('address')
            admin.gender = form.cleaned_data.get('gender')

            password = form.cleaned_data.get('password')
            if password:
                admin.set_password(password)

            if request.FILES.get('profile_pic'):
                fs = FileSystemStorage()
                file = fs.save(
                    request.FILES['profile_pic'].name,
                    request.FILES['profile_pic']
                )
                admin.profile_pic = fs.url(file)

            admin.save()
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect(reverse('student_view_profile'))

        messages.error(request, "Invalid Data Provided")

    return render(request, 'student_template/student_view_profile.html', {
        'form': form,
        'page_title': 'My Profile'
    })


@csrf_exempt
def student_fcmtoken(request):
    try:
        user = get_object_or_404(CustomUser, id=request.user.id)
        user.fcm_token = request.POST.get('token')
        user.save()
        return HttpResponse("True")
    except Exception:
        return HttpResponse("False")


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


def student_view_result(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('-created_at')
    context = {
        'results': results,
        'page_title': 'View Results'
    }
    return render(request, "student_template/student_view_result.html", context)
