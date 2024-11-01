import logging, json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.forms.models import model_to_dict
from ..models.user import User
from ..utlis.auth_helper import validate_password, encode_jwt
from ..constants import UserRoles


@require_POST
def register(request):
    try:
        request_body = json.loads(request.body)
        email = request_body.get("email")
        password = request_body.get("password")
        first_name = request_body.get("first_name", "")
        last_name = request_body.get("last_name", "")
        role = request_body.get("role", UserRoles.STUDENT.value)

        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status = 400)
        
        if not first_name or not last_name:
            return JsonResponse({"error": "First name and last name are required."}, status = 400)
        
        try:
            validate_email(email)
        except:
            return JsonResponse({"error": "Invalid email address."}, status=400)

        user_obj = User.objects.filter(email=email).exists()
        if user_obj:
            return JsonResponse({"error": "Email is already registered."}, status = 400)

        is_password_valid, message = validate_password(password)
        if not is_password_valid:
            return JsonResponse({"error": message}, status = 400)

        hashed_password = make_password(password)

        user = User.objects.create(email=email, password=hashed_password, first_name=first_name, last_name=last_name, role=role)

        return JsonResponse({"message": "User registered successfully", "data": user.id}, status=201)
    except Exception as e:
        logging.error("error while registering user - ", e)
        return JsonResponse({"message": "Unable to register. Please contact Administrator."}, status=201)


@require_POST
def login(request):
    try:
        request_body = json.loads(request.body)
        email = request_body.get("email")
        password = request_body.get("password")
        
        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status = 400)

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "User with given email is not registered. Please sign-up."}, status=400)

        if not check_password(password, user_obj.password):
            return JsonResponse({"error": "Invalid Password."}, status=400)

        token = encode_jwt(user_id=user_obj.id, role=user_obj.role)
        user = model_to_dict(user_obj, fields=['id', 'email', 'first_name', 'last_name'])

        return JsonResponse({"message": "User logged in successfully", "data": user, "token": token}, status=200)

    except Exception as e:
        logging.error("error while logging in user - ", e)
        return JsonResponse({"message": "Unable to login. Please contact Administrator."}, status=201)