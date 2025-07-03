from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Habit, Subscription
from .services import create_or_update_notification, days_of_week_to_crontab
from .tasks import send_telegram_notification

User = get_user_model()


class HabitViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "location": "Home",
            "time": "10:00:00",
            "action": "Read a book",
            "frequency": 3,
            "execution_time": 30,
            "public_indicator": True,
        }

        self.habit = Habit.objects.create(user=self.user, **self.habit_data)

    def test_create_habit(self):
        """Тест создания привычки"""
        # Проверяем начальное количество привычек и подписок
        initial_habits_count = Habit.objects.count()
        initial_subscriptions_count = Subscription.objects.count()

        self.habit_data_create = {
            "location": "Home",
            "time": "10:00:00",
            "action": "Read a book",
            "frequency": 3,
            "execution_time": 30,
            "public_indicator": True,
        }
        url = reverse("tracker:habit-list-create")
        response = self.client.post(url, self.habit_data_create, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что создалась только одна новая привычка
        self.assertEqual(Habit.objects.count(), initial_habits_count + 1)
        # Проверяем, что создалась только одна новая подписка
        self.assertEqual(Subscription.objects.count(), initial_subscriptions_count + 1)

    def test_list_habits(self):
        """Тест получения списка привычек"""
        url = reverse("tracker:habit-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_habit(self):
        """Тест обновления привычки"""
        url = reverse("tracker:habit-detail", kwargs={"pk": self.habit.pk})
        updated_data = self.habit_data.copy()
        updated_data["action"] = "Write code"

        response = self.client.put(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Write code")


class ServicesTests(TestCase):
    def test_days_of_week_to_crontab(self):
        """Тест конвертации частоты в формат crontab"""
        test_cases = [
            (1, "0"),  # Sunday
            (2, "0,3"),  # Sunday, Wednesday
            (3, "0,2,4"),  # Sunday, Tuesday, Thursday
            (7, "0,1,2,3,4,5,6"),  # All days
        ]

        for frequency, expected in test_cases:
            result = days_of_week_to_crontab(frequency)
            self.assertEqual(result, expected)

    @patch("tracker.services.CrontabSchedule")
    @patch("tracker.services.PeriodicTask")
    def test_create_or_update_notification(self, mock_periodic_task, mock_crontab):
        """Тест создания/обновления уведомления"""
        mock_schedule = MagicMock()
        mock_crontab.objects.get_or_create.return_value = (mock_schedule, True)
        # Создаем более полный мок объект подписки
        subscription = MagicMock()
        subscription.id = 1
        subscription.habit.action = "Test Action"
        subscription.habit.location = "Test Location"
        subscription.send_time.strftime.return_value = "10:00"
        subscription.days_of_week = "0,1,2"
        subscription.status = "active"
        create_or_update_notification(subscription)
        mock_periodic_task.objects.update_or_create.assert_called_once()


class TasksTests(TestCase):
    @patch("tracker.tasks.requests.post")
    def test_send_telegram_notification(self, mock_post):
        """Тест отправки уведомления в Telegram"""
        user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )

        habit = Habit.objects.create(
            user=user,
            location="Home",
            time="10:00:00",
            action="Read a book",
            frequency=3,
            execution_time=30,
        )

        subscription = Subscription.objects.create(
            habit=habit,
            send_time=timezone.now().time(),
            status="active",
            days_of_week="0,1,2",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = send_telegram_notification(subscription.id)

        self.assertTrue(result)
        mock_post.assert_called_once()

        subscription.refresh_from_db()
        self.assertEqual(subscription.status, "active")
        self.assertEqual(subscription.notification_count, 1)
