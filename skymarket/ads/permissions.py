from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):  # разрешение на уровне пользователя
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):    # разрешение на уровне объекта
        return request.user.role == UserRoles.ADMIN


class IsOwner(BasePermission):
    def has_permission(self, request, view):    # разрешение на уровне пользователя
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):    # разрешение на уровне объекта
        return request.user and request.user and obj.author == request.user
