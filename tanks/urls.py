from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TankViewSet

router = DefaultRouter()
router.register(r'tanks', TankViewSet, basename='tanks')

urlpatterns = [
    path('', include(router.urls)),
]