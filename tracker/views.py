from rest_framework import generics, permissions
from .models import Habit
from .pagination import HabitPagination
from .serializers import HabitSerializer


class IsOwner(permissions.BasePermission):
    """
    Пользовательское разрешение для проверки владельца привычки
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination
    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя
        """
        return Habit.objects.filter(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя
        """
        return Habit.objects.filter(user=self.request.user)