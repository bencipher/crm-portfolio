from django.urls import path, include
from .views import CustomUserViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', CustomUserViewset, basename='user')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]
