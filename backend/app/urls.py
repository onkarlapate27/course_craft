from django.urls import path
from .views import user_view, course_view

urlpatterns = [
    path('register', view=user_view.register, name='register-user'),
    path('login', view=user_view.login, name='login-user'),
    path('courses', view=course_view.get_courses, name='list-courses'),
    path('courses/create', view=course_view.create_course, name='create-courses'),
    path('courses/<int:course_id>', view=course_view.update_course, name='update-course'),
    path('courses/delete/<int:course_id>', view=course_view.delete_course, name='delete-course'),
]