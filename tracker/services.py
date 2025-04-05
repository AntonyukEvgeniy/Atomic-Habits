import json


def create_or_update_notification(subscription):
    """
    Creates or updates a periodic task for a Subscription instance with timezone support
    Args:
        subscription: Subscription model instance
    """
    try:
        from django_celery_beat.models import PeriodicTask, CrontabSchedule

        # Get days of week string directly (already in correct format)
        days_of_week = subscription.days_of_week

        # Create or get crontab schedule using Moscow time directly
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=subscription.send_time.minute,
            hour=subscription.send_time.hour,
            day_of_week=days_of_week,
            day_of_month='*',
            month_of_year='*',
            timezone='Europe/Moscow'
        )

        # Task name format: notification_task_{subscription_id}
        task_name = f'notification_task_{subscription.id}'
        # Create or update periodic task
        task, created = PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                'crontab': schedule,
                'task': 'tracker.tasks.send_telegram_notification',
                'kwargs': json.dumps({'subscription_id': subscription.id}),
                'enabled': subscription.status == 'active'
            }
        )
    except Exception as e:
        raise e

def days_of_week_to_crontab(frequency):
    """
    Converts frequency to crontab format string for days of week (0-6, where 0 is Sunday)
    Args:
        frequency: Number of days per week (1-7)
    Returns:
        Crontab format string
    """
    if frequency==1:
        day_of_week = '0'  # Sunday
    elif frequency==2:
        day_of_week = '0,3'  # Sunday, Wednesday
    elif frequency==3:
        day_of_week = '0,2,4'  # Sunday, Tuesday, Thursday
    elif frequency==4:
        day_of_week = '0,2,4,6'  # Sunday, Tuesday, Thursday, Saturday
    elif frequency==5:
        day_of_week = '0,1,3,5,6'  # Sunday, Monday, Wednesday, Friday, Saturday
    elif frequency==6:
        day_of_week = '0,1,2,3,4,6'  # All days except Friday
    elif frequency==7:
        day_of_week = '0,1,2,3,4,5,6'  # All days
    return day_of_week


