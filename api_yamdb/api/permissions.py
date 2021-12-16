from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import UserRoles


class AuthorOrReadOnly(BasePermission):
    """Это разрешение представляет права на получение объектов
    любым пользователям, добавления объекта аутентифицированным
    пользователям и редактирования объекта только авторам объекта,
    админу или модераторам
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == UserRoles.MODERATOR
            or request.user.role == UserRoles.ADMIN
            or request.user.is_superuser
        )


class IsAdmin(BasePermission):
    """Пермишн только для админа."""

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.auth and request.user.role == UserRoles.ADMIN
        )


class IsAdminOrReadOnly(BasePermission):
    """ Пермишен для админа на редактирование контента:
        категорий, жанров, произведений.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == UserRoles.ADMIN
                or request.user.is_superuser
            )
        )
