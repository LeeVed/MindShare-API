from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """Только суперпользователь (is_superuser=True)"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsModerator(permissions.BasePermission):
    """Проверка принадлежности к группе модераторов"""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )


class IsOwner(permissions.BasePermission):
    """Проверка, что пользователь — владелец объекта"""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.owner == request.user
        )
