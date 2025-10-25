from functools import wraps
from django.shortcuts import redirect

def is_admin_or_redirect(view_func):
    """
    Decorator that redirects non-staff users to the student dashboard.
    """
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def is_student_or_redirect(view_func):
    """
    Decorator that redirects staff users to the admin dashboard.
    """
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper_func
