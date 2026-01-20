from django.urls import path
<<<<<<< HEAD
from main_app.EditResultView import EditResultView
from . import hod_views, staff_views, student_views, views

#admin home

#add staff
#add student
#add course
#add subject
#add session

#manage staff
#manage student
#manage course
#manage subject
#manage session


#edit staff
#edit student
#edit course
#edit subject
#edit session

#delete staff
#delete student
#delete course
#delete subject
#delete session

#check email availability

#student feedback message
#staff feedback message

#view staff leave
#view student leave

#admin view attendance
#get admin attendance
#admin view profile
#admin notify staff
#admin notify student

#admin send student notification
#admin send staff notification

=======
from . import staff_views, student_views
>>>>>>> d0e6680 (Update urls for backend features)

urlpatterns = [
    # path("", views.login_page, name='login_page'),
    # path("get_attendance", views.get_attendance, name='get_attendance'),
    # path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    # path("doLogin/", views.doLogin, name='user_login'),
    # path("logout_user/", views.logout_user, name='user_logout'),

    path("admin/home/", hod_views.admin_home, name = 'admin_home'),
    path("staff/add", hod_views.add_staff, name = 'add_staff'),
    path("course/add", hod_views.add_course, name ='add_course'),
    path("add_session/", hod_views.add_session, name= 'add_session'),
    path("admin_view_profile", hod_views.admin_view_profile, name= 'admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability, name ="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name ='manage_session'),
    path("session/edit/<int:session_id>", hod_views.edit_session, name='edit_session'),
    path("student/view/feedback/", hod_views.student_feedback_message, name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message, name="staff_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave, name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave, name = "view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance, name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance, name='get_admin_attendance'),
    path("student/add/", hod_views.add_student, name = 'add_student'),
    path("subject/add/", hod_views.add_subject, name ='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name ='manage_staff'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name = 'edit_staff'),
    path("staff/delete/<int:staff_id>", hod_views.delete_staff, name = 'delete_staff'),
    path("course/delete/<int:course_id>", hod_views.delete_course, name='delete_course'),
    path("subject/delete/<int:subject_id>", hod_views.delete_subject, name='delete_subject'),
    path("session/delete/<int:session_id>", hod_views.delete_session, name='delete_session'),
    path("student/delete/<int:student_id>", hod_views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>", hod_views.edit_student, name ='edit_student'),
    path("course/edit/<int:course_id>", hod_views.edit_course, name ='edit_course'),
    path("subject/edit/<int:subject_id>", hod_views.edit_subject, name ='edit_subject'),

    # path("send_student_notification/", hod_views.send_student_notification, name='send_student_notification'),
    # path("send_staff_notification/", hod_views.send_staff_notification, name='send_staff_notification'),
    # path("admin_notify_student", hod_views.admin_notify_student, name='admin_notify_student'),
    # path("admin_notify_staff", hod_views.admin_notify_staff, name='admin_notify_staff'),
]
