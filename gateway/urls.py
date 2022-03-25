from django.urls import path
from .views import GetSecuredInfo, LoginView, RefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name="user-login"),
    path('refresh/', RefreshView.as_view(), name="refresh-token"),
    path('secureinfo/', GetSecuredInfo.as_view(), name="secure-info"),
]
