from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegistrationSerializer
class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)