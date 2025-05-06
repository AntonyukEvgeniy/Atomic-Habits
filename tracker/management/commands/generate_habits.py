from datetime import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from tracker.models import Habit

User = get_user_model()


class Command(BaseCommand):
    help = "Создает привычки для указанного пользователя"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Username пользователя")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
            # Привычка 1: Утренняя зарядка
            Habit.objects.create(
                user=user,
                location="Дом",
                time=time(6, 0),  # 6:00 AM
                action="Сделать зарядку",
                pleasant_habit_indicator=False,
                frequency=7,  # каждый день
                reward="Чашка любимого кофе",
                execution_time=15,
                public_indicator=True,
            )
            # Привычка 2: Чтение книги (приятная привычка)
            habit2 = Habit.objects.create(
                user=user,
                location="Гостиная",
                time=time(20, 0),  # 8:00 PM
                action="Читать книгу",
                pleasant_habit_indicator=True,
                frequency=3,
                execution_time=30,
                public_indicator=False,
            )
            # Привычка 3: Медитация со связанной приятной привычкой
            Habit.objects.create(
                user=user,
                location="Спальня",
                time=time(22, 0),  # 10:00 PM
                action="Медитировать",
                pleasant_habit_indicator=False,
                frequency=5,
                related_habit=habit2,  # связываем с чтением книги
                execution_time=10,
                public_indicator=True,
            )
            # Привычка 4: Тренировка
            Habit.objects.create(
                user=user,
                location="Спортзал",
                time=time(22, 0),  # 10:00 PM
                action="Тренироваться",
                pleasant_habit_indicator=False,
                frequency=3,
                reward="Покушать пиццу",
                execution_time=45,
                public_indicator=False,
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Пользователь с username {username} не найден")
            )
        self.stdout.write(
            self.style.SUCCESS(f"Привычки успешно созданы для пользователя {username}")
        )
