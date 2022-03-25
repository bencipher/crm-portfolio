from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        try:
            user = CustomUser(**validated_data)
            user.save()
            user.set_password(password)
        except Exception as e:
            raise Exception(str(e))
        return user
