import datetime

from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import CustomUser, Follow

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .serializers import (FavAndCartSerializer, FollowSerializer,
                          IngredientListSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)


class UsersViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny, )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        follows = CustomUser.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(follows)
        if pages:
            serializer = FollowSerializer(
                pages, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        follow_to = get_object_or_404(CustomUser, id=id)
        subscription = Follow.objects.filter(user=user, following=follow_to)
        if request.method == 'POST' and user.username != follow_to.username:
            Follow.objects.get_or_create(user=user, following=follow_to)
            serializer = FollowSerializer(
                follow_to, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE' and subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error':
                'Вы не подписаны на данного пользователя '
                'или подписываетесь на себя!'},
            status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', )


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            serializer = FavAndCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        to_buy = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        to_buy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__purchases__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
        main_list = ([
            f"* {item}:{value['amount']}"
            f"{value['measurement_unit']}\n"
            for item, value in shopping_list.items()]
        )
        today = datetime.date.today()
        main_list.append(f'\n aboba, {today.year}')
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            Favorite.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            serializer = FavAndCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
