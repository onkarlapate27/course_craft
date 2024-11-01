import jwt
from django.http import JsonResponse
from .models.user import User
from ..courses.config_settings import settings

def auth_middleware(get_response):
    def middleware(request):
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, settings.get('JWT_SECRET'), algorithms=[settings.get('JWT_ALGORITHM')])
                user = User.objects.get(id=payload['user_id'])
                request.user = user
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
        else:
            request.user = None

        response = get_response(request)
        return response
    return middleware
