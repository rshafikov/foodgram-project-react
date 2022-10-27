from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
from .models import IngredientAmount, Tag, Ingredient, Recipe, Favorite, ShoppingCart
from drf_extra_fields.fields import Base64ImageField
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

class IngredientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')

class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    name = serializers.SlugRelatedField(
        slug_field='name',
        source='ingredient',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        slug_field='measurement_unit',
        source='ingredient',
        read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('amount', 'id')


class RecipeImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_in_shopping_cart',
            'name',  'text', 'cooking_time', 'image', 'is_favorited'
        )

    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.recipe_ingredients.all()
        return IngredientSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True, max_length=None)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name',  'text', 'cooking_time', 'image'
        )
    
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.save()
        recipe.tags.set(tags)
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['ingredient'],
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in ingredients])
        return recipe
    
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        IngredientAmount.objects.filter(recipe=instance).delete()
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['ingredient'],
            recipe=instance,
            amount=ingredient['amount']
        ) for ingredient in ingredients])
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.save()
        instance.tags.set(tags_data)
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients': ('Число игредиентов должно быть больше 0')
                })
        return data

    def validate_cooking_time(self, data):
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0'
            )
        return data

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data

class FavAndCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ('id','name', 'image', 'cooking_time')
