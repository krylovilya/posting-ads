from rest_framework import permissions


class UserIsObjectOwnerPermission(permissions.BasePermission):
    """Проверяет, есть ли у пользователя доступ к объекту"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller.user_id == request.user.id
