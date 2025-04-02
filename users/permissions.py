from rest_framework import permissions
class IsOwnerOrPublic(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее:
    - владельцам привычки видеть свои привычки (публичные и приватные)
    - всем пользователям видеть публичные привычки
    """
    def has_object_permission(self, request, view, obj):
        # Проверяем является ли привычка публичной
        if obj.public_indicator:
            return True
        # Проверяем является ли пользователь владельцем
        return obj.user == request.user