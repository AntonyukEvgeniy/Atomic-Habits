import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask


def create_or_update_notification(subscription):
    """
    Создает или обновляет периодическую задачу для экземпляра Подписки с поддержкой часового пояса
    Аргументы:
        subscription: экземпляр модели Subscription
    """

    days_of_week = subscription.days_of_week
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=subscription.send_time.minute,
        hour=subscription.send_time.hour,
        day_of_week=days_of_week,
        day_of_month="*",
        month_of_year="*",
        timezone="Europe/Moscow",
    )

    task_name = f"notification_task_{subscription.id}"
    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            "crontab": schedule,
            "task": "tracker.tasks.send_telegram_notification",
            "kwargs": json.dumps({"subscription_id": subscription.id}),
            "enabled": subscription.status == "active",
        },
    )


def days_of_week_to_crontab(frequency):
    """
    Преобразует частоту в строку формата crontab для дней недели (0-6, где 0 - воскресенье)
    Аргументы:
        frequency: Количество дней в неделю (1-7)
    Возвращает:
        Строка в формате crontab
    """
    if frequency == 1:
        day_of_week = "0"  # Воскресенье
    elif frequency == 2:
        day_of_week = "0,3"  # Воскресенье, Среда
    elif frequency == 3:
        day_of_week = "0,2,4"  # Воскресенье, Вторник, Четверг
    elif frequency == 4:
        day_of_week = "0,2,4,6"  # Воскресенье, Вторник, Четверг, Суббота
    elif frequency == 5:
        day_of_week = "0,1,3,5,6"  # Воскресенье, Понедельник, Среда, Пятница, Суббота
    elif frequency == 6:
        day_of_week = "0,1,2,3,4,6"  # Все дни кроме пятницы
    elif frequency == 7:
        day_of_week = "0,1,2,3,4,5,6"  # Каждый день
    return day_of_week
