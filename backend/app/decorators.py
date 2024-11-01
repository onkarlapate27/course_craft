from django.http import HttpResponse
from functools import wraps

def auth_decorator(view_func):
    @wraps(view_func)
    def deco(request, *args, **kwargs):
        if not request.user:
            return HttpResponse({"error": "Authentication required"}, status=401)
        return view_func(request, *args, **kwargs)
    return deco