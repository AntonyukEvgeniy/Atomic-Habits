from django.urls import path

from . import views

app_name = "tracker"
urlpatterns = [
    path("habits/", views.HabitListCreateView.as_view(), name="habit-list-create"),
    path("habits/<int:pk>/", views.HabitDetailView.as_view(), name="habit-detail"),
    path(
        "subscriptions/<int:subscription_id>/trigger/",
        views.trigger_subscription_notification,
        name="trigger-notification",
    ),
]
