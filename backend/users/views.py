from djoser.views import UserViewSet
from rest_framework import mixins
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer