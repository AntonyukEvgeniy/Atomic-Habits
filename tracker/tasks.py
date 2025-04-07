import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from config.settings import TELEGRAM_CHAT_ID

from .models import Subscription


@shared_task
def send_telegram_notification(subscription_id):
    """
    Отправляет уведомление в Telegram с учетом ограничений и расписания
    """
    try:
        notification = Subscription.objects.get(id=subscription_id)

        habit = notification.habit
        message = (
            f"Напоминание о привычке!\n\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.location}\n"
            f"Время: {habit.time}\n"
        )

        response = requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
        )

        if response.status_code == 200:
            notification.status = Subscription.ACTIVE
            notification.notification_count += 1
            notification.last_notification = timezone.now()
            notification.save()
            return True
        else:
            notification.status = Subscription.DEACTIVATED
            notification.save()
            return False

    except Subscription.DoesNotExist:
        return False


@shared_task
def trigger_notification(subscription_id):
    """
    Принудительно запускает отправку уведомления для указанной подписки
    """
    try:
        # Используем существующую логику отправки уведомления
        return send_telegram_notification(subscription_id)
    except Exception as e:
        print(f"Error triggering notification: {e}")
        return False
