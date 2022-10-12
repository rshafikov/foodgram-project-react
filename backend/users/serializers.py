from djoser.serializers import UserCreateSerializer, TokenCreateSerializer
from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

