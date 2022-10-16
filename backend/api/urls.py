from django.urls import path, include
from .views import UsersViewSet, TagViewSet, IngredientViewSet
from rest_framework import routers
# import djoser.urls.authtoken

app_name = 'api'

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
router_v1.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]