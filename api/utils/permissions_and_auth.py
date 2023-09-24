from rest_framework.permissions import BasePermission, SAFE_METHODS


class MyIsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class MyModeratorUser(BasePermission):
    def has_permission(self, request, view):
        if request.method not in ['POST', 'DELETE']:
            return bool(request.user and request.user.is_authenticated and request.user.is_moderator)
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class MyActualUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        obj = view.get_object()
        return request.user and request.user.is_authenticated and obj == request.user

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj == request.user


class MyUserPerm(BasePermission):
    op1 = MyIsAdminUser()
    op2 = MyActualUser()
    op3 = MyModeratorUser()

    def has_permission(self, request, view):
        return (
            self.op1.has_permission(request, view) or
            self.op2.has_permission(request, view) or
            self.op3.has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            self.op1.has_object_permission(request, view, obj)
        ) or (
            self.op2.has_object_permission(request, view, obj)
        ) or (
            self.op3.has_object_permission(request, view, obj)
        )
