from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from users.models import User


class Habit(models.Model):
    """
    Модель привычки
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    location = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")

    pleasant_habit_indicator = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        limit_choices_to={"pleasant_habit_indicator": True},
    )

    frequency = models.PositiveIntegerField(
        verbose_name="Периодичность (раз в неделю)",
        validators=[
            MinValueValidator(
                1, message="Привычка должна выполняться минимум 1 раз в неделю"
            ),
            MaxValueValidator(
                7, message="Привычка не может выполняться реже, чем раз в неделю"
            ),
        ],
        default=1,
    )

    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )

    execution_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        help_text="Время на выполнение не должно превышать 120 секунд",
        verbose_name="Время на выполнение (в минутах)",
    )

    public_indicator = models.BooleanField(
        default=False, verbose_name="Признак публичности"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):

        if self.pleasant_habit_indicator and (self.related_habit or self.reward):
            raise ValidationError(
                "Приятная привычка не может иметь связанную привычку или вознаграждение"
            )

        if not self.pleasant_habit_indicator and not (
            self.related_habit or self.reward
        ):
            raise ValidationError(
                "У привычки должно быть вознаграждение или связанная привычка"
            )

        if self.related_habit and self.reward:
            raise ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение"
            )

    def __str__(self):
        """
        Возвращает отформатированное описание привычки в формате:
        'я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]'
        """
        return f"я буду {self.action} в {self.time.strftime('%H:%M')} в {self.location}"


class Subscription(models.Model):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    STATUS_CHOICES = [
        (ACTIVE, "Уведомления включены"),
        (DEACTIVATED, "Уведомления отключены"),
    ]
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name="subscriptions"
    )
    send_time = models.TimeField("Время отправки")
    status = models.CharField(
        "Статус подписки",
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    notification_count = models.IntegerField(default=0)
    last_notification = models.DateTimeField(null=True, blank=True)
    days_of_week = models.CharField(
        max_length=20,
        verbose_name="Дни недели для отправки",
        help_text="Дни недели в формате 1,2,3,4,5,6,7 (где 1 - понедельник)",
        default="1,2,3,4,5,6,7",
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"Подписка на {self.habit} ({self.status})"
