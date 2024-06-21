import uuid
import jwt
import datetime
from decouple import config
from rest_framework import authentication
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def create_auth_token(user):
    pay_load = {
        'id': f"{user.id}",
        'name': f"{user.firstname} {user.lastname}",
        'email': f"{user.email}",
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(pay_load, config('JWT_SECRET'), algorithm='HS256')
    return token


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if not auth_token:
            return None
        try:
            pay_load = jwt.decode(auth_token, config('JWT_SECRET'), algorithms=['HS256'], options={'exp': datetime.timedelta(minutes=60)})
        except jwt.InvalidTokenError or jwt.InvalidSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Login Again...')
        _id = uuid.UUID(pay_load['id'])
        user = User.objects.get(id=_id)
        if user is not None and user.is_active:
            return user, None
        elif not user.is_active:
            raise AuthenticationFailed('Not authenticated')
        else:
            return None
