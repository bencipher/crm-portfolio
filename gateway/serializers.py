from rest_framework import serializers
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
