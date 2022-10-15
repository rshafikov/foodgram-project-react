from dataclasses import field
from djoser.serializers import UserCreateSerializer
from users.models import CustomUser, Tag
from rest_framework.serializers import ModelSerializer


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')