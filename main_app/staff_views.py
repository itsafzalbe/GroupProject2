import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


# staff home
# staff take attendance
# get studentes
# save attendance
# staff update attendance
# get student attendance
# update attendance
# staff apply leave
# staff feedback
# staff view profile
# staff fcm token
# staff view notification <- not needed, (anything related to notifications)
# staff add result
# fetch student result


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)

    subjects = Subject.objects.filter(staff=staff)
    total_students = Student.objects.filter(course=staff.course).count()
    total_subject = subjects.count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()

    attendance_list = []
    subject_list = []

    for subject in subjects:
        count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name)
        attendance_list.append(count)

    context = {
        'page_title': f"Staff Panel - {staff.admin.last_name} ({staff.course})",
        'total_students': total_students,
        'total_subject': total_subject,
        'total_leave': total_leave,
        'attendance_list': attendance_list,
        'subject_list': subject_list
    }
    return render(request, 'staff_template/home_content.html', context)


def staff_take_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    context = {
        'subjects': Subject.objects.filter(staff=staff),
        'sessions': Session.objects.all(),
        'page_title': 'Take Attendance'
    }
    return render(request, 'staff_template/staff_take_attendance.html', context)


@csrf_exempt
def get_students(request):
    subject = get_object_or_404(Subject, id=request.POST.get('subject'))
    session = get_object_or_404(Session, id=request.POST.get('session'))

    students = Student.objects.filter(course=subject.course, session=session)
    data = [{
        "id": s.id,
        "name": f"{s.admin.last_name} {s.admin.first_name}"
    } for s in students]

    return JsonResponse(json.dumps(data), safe=False)


@csrf_exempt
def save_attendance(request):
    students = json.loads(request.POST.get('student_ids'))
    subject = get_object_or_404(Subject, id=request.POST.get('subject'))
    session = get_object_or_404(Session, id=request.POST.get('session'))
    date = request.POST.get('date')

    attendance, _ = Attendance.objects.get_or_create(
        subject=subject,
        session=session,
        date=date
    )

    for s in students:
        student = get_object_or_404(Student, id=s['id'])
        report, created = AttendanceReport.objects.get_or_create(
            student=student,
            attendance=attendance
        )
        if created:
            report.status = s['status']
            report.save()

    return HttpResponse("OK")


def staff_update_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    return render(request, 'staff_template/staff_update_attendance.html', {
        'subjects': Subject.objects.filter(staff=staff),
        'sessions': Session.objects.all(),
        'page_title': 'Update Attendance'
    })


@csrf_exempt
def get_student_attendance(request):
    attendance = get_object_or_404(Attendance, id=request.POST.get('attendance_date_id'))
    reports = AttendanceReport.objects.filter(attendance=attendance)

    data = [{
        "id": r.student.admin.id,
        "name": f"{r.student.admin.last_name} {r.student.admin.first_name}",
        "status": r.status
    } for r in reports]

    return JsonResponse(json.dumps(data), safe=False)


@csrf_exempt
def update_attendance(request):
    attendance = get_object_or_404(Attendance, id=request.POST.get('date'))
    students = json.loads(request.POST.get('student_ids'))

    for s in students:
        student = get_object_or_404(Student, admin_id=s['id'])
        report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
        report.status = s['status']
        report.save()

    return HttpResponse("OK")


def staff_apply_leave(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = LeaveReportStaffForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        leave = form.save(commit=False)
        leave.staff = staff
        leave.save()
        messages.success(request, "Leave applied successfully")
        return redirect('staff_apply_leave')

    return render(request, 'staff_template/staff_apply_leave.html', {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(staff=staff),
        'page_title': 'Apply Leave'
    })


def staff_feedback(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = FeedbackStaffForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        feedback.staff = staff
        feedback.save()
        messages.success(request, "Feedback submitted")
        return redirect('staff_feedback')

    return render(request, 'staff_template/staff_feedback.html', {
        'form': form,
        'feedbacks': FeedbackStaff.objects.filter(staff=staff),
        'page_title': 'Feedback'
    })


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None, instance=staff)

    if request.method == 'POST' and form.is_valid():
        admin = staff.admin
        admin.first_name = form.cleaned_data['first_name']
        admin.last_name = form.cleaned_data['last_name']
        admin.address = form.cleaned_data['address']
        admin.gender = form.cleaned_data['gender']

        if form.cleaned_data.get('password'):
            admin.set_password(form.cleaned_data['password'])

        if request.FILES.get('profile_pic'):
            fs = FileSystemStorage()
            file = fs.save(request.FILES['profile_pic'].name, request.FILES['profile_pic'])
            admin.profile_pic = fs.url(file)

        admin.save()
        staff.save()
        messages.success(request, "Profile Updated")
        return redirect('staff_view_profile')

    return render(request, 'staff_template/staff_view_profile.html', {
        'form': form,
        'page_title': 'Profile'
    })


@csrf_exempt
def staff_fcmtoken(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    user.fcm_token = request.POST.get('token')
    user.save()
    return HttpResponse("True")


def staff_add_result(request):
    staff = get_object_or_404(Staff, admin=request.user)

    if request.method == 'POST':
        student = get_object_or_404(Student, id=request.POST.get('student_list'))
        subject = get_object_or_404(Subject, id=request.POST.get('subject'))

        result, _ = StudentResult.objects.get_or_create(student=student, subject=subject)
        result.test = request.POST.get('test')
        result.exam = request.POST.get('exam')
        result.save()
        messages.success(request, "Result Saved")

    return render(request, 'staff_template/staff_add_result.html', {
        'subjects': Subject.objects.filter(staff=staff),
        'sessions': Session.objects.all(),
        'page_title': 'Add Result'
    })


@csrf_exempt
def fetch_student_result(request):
    student = get_object_or_404(Student, id=request.POST.get('student'))
    subject = get_object_or_404(Subject, id=request.POST.get('subject'))

    result = StudentResult.objects.get(student=student, subject=subject)
    return HttpResponse(json.dumps({
        'test': result.test,
        'exam': result.exam
    }))


def staff_dashboard(request):  # chala
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
