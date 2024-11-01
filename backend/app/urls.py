from django.urls import path
from .views import user_view, course_view

urlpatterns = [
    path('register', view=user_view.register, name='register-user'),
    path('login', view=user_view.login, name='login-user')
]