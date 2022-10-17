from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
from .models import Tag, Ingredient
from rest_framework.serializers import ModelSerializer, SerializerMethodField, Field


class CustomUserSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.following.filter(user=user).exists()

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


# class SubscribeSerilizer:
#     pass


class FollowSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    # recipes = 
    # recipes_count = 

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.following.filter(user=user).exists()
