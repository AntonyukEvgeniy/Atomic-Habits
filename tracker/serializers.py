from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"

    @staticmethod
    def validate_frequency(value):
        if value < 1 or value > 7:
            raise serializers.ValidationError(
                "Периодичность привычки должна быть от 1 до 7 раз в неделю"
            )
        return value

    @staticmethod
    def validate_related_habit(value):
        if value is not None:
            try:
                habit = Habit.objects.get(id=value.id)
                if not habit.pleasant_habit_indicator:
                    raise serializers.ValidationError(
                        "Связанная привычка должна быть приятной"
                    )
            except Habit.DoesNotExist:
                raise serializers.ValidationError(
                    "Указанная связанная привычка не существует"
                )
        return value
    @staticmethod
    def validate_execution_time(value):
        if value > 120:
            raise serializers.ValidationError(
                "Время выполнения привычки не может превышать 120 секунд"
            )
        return value

    def validate(self, data):
        reward = data.get('reward')
        related_habit = data.get('related_habit')
        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку"
            )
        # Проверка связанных привычек
        if data.get('related_habit') and not data['related_habit'].pleasant_habit_indicator:
            raise serializers.ValidationError(
                "В связанные привычки можно добавлять только приятные привычки"
            )
        # Проверка приятных привычек
        if data.get('pleasant_habit_indicator'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )
        return data