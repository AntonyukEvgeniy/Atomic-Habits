from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"

    def validate_frequency(self, value):
        if value < 1 or value > 7:
            raise serializers.ValidationError(
                "Периодичность привычки должна быть от 1 до 7 раз в неделю"
            )
        return value
