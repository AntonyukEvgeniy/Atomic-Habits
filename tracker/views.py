from rest_framework import generics, permissions
from users.permissions import IsOwnerOrPublic
from .models import Habit, Subscription
from .pagination import HabitPagination
from .serializers import HabitSerializer
from .services import create_or_update_notification, days_of_week_to_crontab
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import trigger_notification


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrPublic]
    pagination_class = HabitPagination

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя
        """
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        subscription = Subscription.objects.create(
            habit=habit,
            send_time=habit.time,
            status="active",
            days_of_week=days_of_week_to_crontab(habit.frequency),
        )
        subscription.save()
        create_or_update_notification(subscription)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrPublic]

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя
        """
        return Habit.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        habit = serializer.save()
        # Обновляем связанную подписку
        subscription = Subscription.objects.filter(habit=habit).first()
        if subscription:
            subscription.send_time = habit.time
            subscription.save()
            create_or_update_notification(subscription)


@api_view(["POST"])
def trigger_subscription_notification(request, subscription_id):
    """
    Принудительно запускает отправку уведомления для подписки
    """
    task = trigger_notification.delay(subscription_id)
    return Response({"task_id": task.id})
