from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
from .models import IngredientAmount, Tag, Ingredient, Recipe
from rest_framework import serializers


class CustomUserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and obj.following.filter(user=user).exists()
        )


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and obj.following.filter(user=user).exists()
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            read_only=True)
    name = serializers.SlugRelatedField(slug_field='name',
                                        source='ingredient',
                                        read_only=True)
    measurement_unit = serializers.SlugRelatedField(
        slug_field='measurement_unit',
        source='ingredient', read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('amount', 'id')


class RecipeShortSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField()
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name',  'description', 'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.recipe_ingredients.all()
        return IngredientSerializer(queryset, many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id','ingredients', 'name', 'author', 'description', 'cooking_time', 'tags') # 'image', 'tags'
        
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.save()
        recipe.tags.set(tags)
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ing['ingredient'],
            recipe=recipe,
            amount=ing['amount']
        ) for ing in ingredients])
        return recipe

    def to_representation(self, instance):
        data = RecipeShortSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


