from rest_framework.permissions import BasePermission, SAFE_METHODS
from api import models


class MyAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser:
            try:
                obj = view.get_object()
            except AssertionError:
                obj = None

            if obj != request.user and isinstance(obj, models.User) and obj.is_superuser:
                return False
            return True
        return False


class MyModeratorUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_moderator:
            try:
                obj = view.get_object()
            except AssertionError:
                obj = None

            if obj == request.user:
                return True

            if getattr(obj, 'user', None) == request.user:
                return True

            if isinstance(obj, models.User) and (obj.is_superuser or obj.is_moderator):
                return False

            if request.method not in ['POST', 'DELETE']:
                return True
            return False

        return False


class MyCounselor(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_counselor:
            try:
                obj = view.get_object()
            except AssertionError:
                obj = None

            if obj == request.user:
                return True

            if getattr(obj, 'user', None) == request.user:
                return True

            if request.method in SAFE_METHODS:
                if isinstance(obj, models.User) and not obj.is_superuser:
                    return True
            return False

        return False


class MyRegularUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_regular_user:
            try:
                obj = view.get_object()
            except AssertionError:
                obj = None

            if obj == request.user:
                return True

            if getattr(obj, 'user', None) == request.user:
                return True

            if request.method in SAFE_METHODS:
                if isinstance(obj, models.User) and not obj.is_superuser:
                    return True
            return False

        return False


class MyUserPerm(BasePermission):
    op1 = MyAdminUser()
    op2 = MyModeratorUser()
    op3 = MyCounselor()
    op4 = MyRegularUser()

    def has_permission(self, request, view):
        return (
            self.op1.has_permission(request, view) or
            self.op2.has_permission(request, view) or
            self.op3.has_permission(request, view) or
            self.op4.has_permission(request, view)
        )
