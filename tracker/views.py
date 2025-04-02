from rest_framework import generics, permissions

from users.permissions import IsOwnerOrPublic
from .models import Habit
from .pagination import HabitPagination
from .serializers import HabitSerializer


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrPublic]
    pagination_class = HabitPagination
    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя
        """
        return Habit.objects.filter(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrPublic]

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя
        """
        return Habit.objects.filter(user=self.request.user)