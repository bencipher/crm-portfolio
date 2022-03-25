import jwt
from .auth import Authentication
from .models import Jwt
from django.contrib.auth import get_user_model, authenticate
from datetime import datetime, timedelta
from django.conf import settings
import string
import random
from .serializers import LoginSerializer, RefreshSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length)) + '$'


def get_access_token(payload):
    return jwt.encode({"exp": datetime.now() + timedelta(minutes=5), "data": payload, }, settings.SECRET_KEY,
                      algorithm='HS256')


def get_refresh_token():
    return jwt.encode({"exp": datetime.now() + timedelta(days=365), "data": get_random(10)}, settings.SECRET_KEY,
                      algorithm='HS256')


class LoginView(APIView):
    """Login Endpoint"""
    serializer_class = LoginSerializer

    def save_jwt(self, user):
        Jwt.objects.filter(user_id=user.id).delete()
        self.access = get_access_token({"user_id": user.id})
        self.refresh = get_refresh_token()
        Jwt.objects.create(user_id=user.id, access=self.access.decode(), refresh=self.refresh.decode())

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)
        # print(email + ' ' + password)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({"error": "Invalid credentials", }, status=status.HTTP_400_BAD_REQUEST)

        self.save_jwt(user)

        return Response({"access": self.access, "refresh": self.refresh}, status=status.HTTP_200_OK)


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data['refresh']
            )
        except Jwt.DoesNotExist:
            return Response({'error': 'Refresh token not found'})

        if not Authentication.verify_token(serializer.validated_data['refresh']):
            return Response({'error': 'Invalid or expired token'})

        access = get_access_token({'user_id': active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access.decode()
        active_jwt.refresh = refresh.decode()
        active_jwt.save()

        return Response({'access': access, 'refresh': refresh})


class GetSecuredInfo(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raise Exception('Tst')
        print(f'Current USER is {request.user}')
        # Authentication.validate_request(request.headers)
        return Response({'data': 'This is a secured info'})
