from django.urls import path, include
from .views import UsersViewSet, TagViewSet
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)
router_v1.register(
    'tags',
    TagViewSet,
    basename='tags'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]