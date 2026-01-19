from django.shortcuts import render
from .models import Student, NotificationStudent

def student_all_notification(request):

    """Talabaga kelgan bildirishnomalarni ko'rsatish"""

    student_obj = Student.objects.get(admin=request.user)
    notifications = NotificationStudent.objects.filter(student=student_obj)
    return render(request, "student_template/all_notification.html", {"notifications": notifications})