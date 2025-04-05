from django.urls import path

from .apps import UsersConfig
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    UserRegistrationView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
