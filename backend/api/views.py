from djoser.views import UserViewSet
from users.models import CustomUser, Follow
from .models import Tag, Ingredient, Recipe
from .serializers import FollowSerializer, RecipeSerializer, TagSerializer, IngredientSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status


class UsersViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny, )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = CustomUser.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(follows)
        if pages:
            serializer = FollowSerializer(pages, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        follow_to = get_object_or_404(CustomUser, id=id)
        subscription = Follow.objects.filter(user=user, following=follow_to)
        if self.request.method == 'POST' and user.username != follow_to.username:
            Follow.objects.get_or_create(user=user, following=follow_to)
            serializer = FollowSerializer(follow_to, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE' and subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error':
                'Вы не подписаны на данного пользователя '
                'или подписываетесь на себя!'
            },
            status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', ) 


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
