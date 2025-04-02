from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from django.core.exceptions import ValidationError

class Habit(models.Model):
    """
    Модель привычки
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    location = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")

    pleasant_habit_indicator = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        limit_choices_to={'pleasant_habit_indicator': True}
    )

    frequency = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (раз в неделю)"
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение"
    )

    execution_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение (в минутах)"
    )

    public_indicator = models.BooleanField(
        default=False,
        verbose_name="Признак публичности"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


    def clean(self):

        if self.pleasant_habit_indicator and (self.related_habit or self.reward):
            raise ValidationError(
                "Приятная привычка не может иметь связанную привычку или вознаграждение"
            )

        if not self.pleasant_habit_indicator and not (self.related_habit or self.reward):
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