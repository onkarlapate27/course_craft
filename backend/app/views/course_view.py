import logging, json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from ..decorators import auth_decorator
from ..models.course import Course
from ..constants import UserRoles


@auth_decorator
@require_http_methods(["GET"])
def get_courses(request):
    try:
        course_id = request.GET.get('course_id')
        courses = []

        if course_id:
            courses = Course.objects.filter(id=course_id)
        else:
            courses = Course.objects.all()

        courses_list = []

        for course in courses:
            course_data = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "created_at": course.created_at,
                "updated_at": course.updated_at,
            }
            courses_list.append(course_data)

        return JsonResponse({"message": "Courses listed successfully.", "data":courses_list})

    except Exception as e:
        logging.error(f"error in listing courses - \n {e}")
        return JsonResponse({"error": "Unable to list courses. Please contact administrator"}, status=400)


@auth_decorator
@require_http_methods(["POST"])
def create_course(request):
    try:
        if request.role != UserRoles.ADMIN.value:
            return JsonResponse({"error": "Course can only be created by admin."}, status=400)

        request_body = json.loads(request.body)
        title = request_body.get("title")
        description = request_body.get("description")

        if not title or not description:
            return JsonResponse({"error": "Course title and description is required."}, status=400)

        is_title_present = Course.objects.filter(title__iexact=title).first()

        if is_title_present:
            return JsonResponse({"error": "Course title already present. Please try a different one."}, status=400)

        course = Course.objects.create(title=title, description=description)

        return JsonResponse({"message": "Course created successfully.", "course_id": course.id}, status=201)

    except Exception as e:
        logging.error(f"Error in creating new course. \n {e}")
        return JsonResponse({"error": "Unable to create course. Please contact administrator"}, status=400)


@auth_decorator
@require_http_methods(["PATCH"])
def update_course(request, course_id):
    try:
        if request.role != UserRoles.ADMIN.value:
            JsonResponse({"error": "Course can only be updated by admin."}, status=400)

        request_body = json.loads(request.body)
        description = request_body.get("description")

        is_course_present = Course.objects.filter(id=course_id).first()

        if not is_course_present:
            return JsonResponse({"error": "Course does not exists."}, status=400)

        if description:
            is_course_present.description = description
            is_course_present.save()

        return JsonResponse({"message": "Course updated successfully."})

    except Exception as e:
        logging.error(f"Error in updating course. \n {e}")
        return JsonResponse({"error": "Unable to update course. Please contact administrator"}, status=400)
    

@auth_decorator
@require_http_methods(["DELETE"])
def delete_course(request, course_id):
    try:
        if request.role != UserRoles.ADMIN.value:
            JsonResponse({"error": "Course can only be updated by admin."}, status=400)

        is_course_present = Course.objects.filter(id=course_id).first()

        if not is_course_present:
            return JsonResponse({"error": "Course does not exists."}, status=400)

        Course.objects.filter(id=course_id).delete()

        return JsonResponse({"message": "Course deleted successfully."})

    except Exception as e:
        logging.error(f"Error in deleting course. \n {e}")
        return JsonResponse({"error": "Unable to delete course. Please contact administrator"}, status=400)


@auth_decorator
@require_http_methods(["POST"])
def purchase_course(request):
    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')

        course = Course.objects.filter(id=course_id).first()
        if not course:
            return JsonResponse({"error": "Course does not exists."}, status=400)
        
        user = request.user
        user.courses_enrolled.add(course)

        return JsonResponse({"message": "Course purchased successfully."})

    except Exception as e:
        logging.error(f"Error in purchasing course. \n {e}")
        return JsonResponse({"error": "Unable to purchase course. Please contact administrator"}, status=400)
    

@auth_decorator
@require_http_methods(["GET"])
def get_purchased_courses(request):
    try:
        user = request.user
        purchased_courses = user.courses_enrolled.all()
        purchased_courses_list = []

        for course in purchased_courses:
            course_obj = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
            }
            purchased_courses_list.append(course_obj)

        return JsonResponse({"message": "Purchased courses listed successfully.", "data": purchased_courses_list})

    except Exception as e:
        logging.error(f"Error in listing purchased courses. \n {e}")
        return JsonResponse({"error": "Unable to get purchased courses. Please contact administrator"}, status=400)