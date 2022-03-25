import jwt
from datetime import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from users.models import CustomUser


class Authentication(BaseAuthentication):

    @staticmethod
    def validate_request(headers):
        authorization = headers.get('Authorization')
        if not authorization:
            return None
            # raise Exception('Invalid Auth')
        token = authorization[7:]
        print(f"Header is {token}")
        decoded_data = Authentication.verify_token(token)


        if not decoded_data:
            return None
            # raise Exception('Token expired or invalid')
        print(decoded_data)
        return decoded_data

    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None

        return self.get_user(data['data']['user_id']), None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except Exception:
            return None
            # raise Exception('User Does Not exist.')

        return user

    @staticmethod
    def verify_token(token):
        try:
            decoded_data = jwt.decode(
                token, settings.SECRET_KEY, algorithm='HS256'
            )
        except Exception:
            return None

        exp = decoded_data['exp']

        if datetime.now().timestamp() > exp:
            return None

        return decoded_data
