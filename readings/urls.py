from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReadingViewSet

router = DefaultRouter()
router.register(r'readings', ReadingViewSet, basename='readings')

urlpatterns = [
    path('', include(router.urls)),
]