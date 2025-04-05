from django.contrib import admin
from django_celery_beat.admin import PeriodicTaskAdmin
from django_celery_beat.models import PeriodicTask
from .models import Subscription
from .tasks import trigger_notification


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'habit', 'send_time', 'status', 'notification_count']
    list_filter = ['status']
    actions = ['trigger_notifications']

    def trigger_notifications(self, request, queryset):
        for subscription in queryset:
            trigger_notification.delay(subscription.id)
        self.message_user(request, f"Запущена отправка уведомлений для {queryset.count()} подписок")

    trigger_notifications.short_description = "Отправить уведомления для выбранных подписок"

