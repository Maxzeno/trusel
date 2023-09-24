from rest_framework.permissions import BasePermission


class MyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser


class MyModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_moderator


class MyCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_counselor


class MyRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_regular_user


class MyOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            obj = view.get_object()
        except Exception as e:
            return False
        return obj == request.user
