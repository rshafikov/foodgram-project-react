from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
from .models import Tag, Ingredient
from rest_framework.serializers import ModelSerializer


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class SubscribeSerilizer(ModelSerializer):
    pass


class FollowSerializer(ModelSerializer):
    is_subscribed = SubscribeSerilizer()
    # recipes = 
    # recipes_count = 

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')