from django.shortcuts import redirect
from django.urls import reverse


class LoginCheckMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if path in [reverse('login_page'), reverse('user_login'), reverse('user_logout')]:
            return self.get_response(request)

        if path.startswith('/admin/'):
            return self.get_response(request)

        if not user.is_authenticated:
            return redirect(reverse('login_page'))

        if user.user_type == '1': 
            if path.startswith('/student/') or path.startswith('/staff/'):
                return redirect(reverse('admin_home'))

        elif user.user_type == '2':
            if path.startswith('/admin/') or path.startswith('/student/'):
                return redirect(reverse('staff_home'))

        elif user.user_type == '3':
            if path.startswith('/admin/') or path.startswith('/staff/'):
                return redirect(reverse('student_home'))

        return self.get_response(request)
    