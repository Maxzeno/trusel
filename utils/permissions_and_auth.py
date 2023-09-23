from rest_framework.permissions import BasePermission

# class MyUserPerm(BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser:
#             return True

#         if request.user and request.user.is_authenticated:
#             return True

#         return False

#     def has_object_permission(self, request, view, obj):
#         if obj == request.user and request.user.is_authenticated:
#             return True

#         if request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser:
#             return True

#         return False


class MyIsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class MyModeratorUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return False
        return bool(request.user and request.user.is_authenticated and request.user.is_moderator)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class MyActualUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user and request.user.is_authenticated


class MyUserPerm:
    def __init__(self):
        self.op1 = MyIsAdminUser
        self.op2 = MyActualUser
        self.op3 = MyModeratorUser

    def has_permission(self, request, view):
        return (
            self.op1.has_permission(request, view) or
            self.op2.has_permission(request, view) or
            self.op3.has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            self.op1.has_permission(request, view)
            and self.op1.has_object_permission(request, view, obj)
        ) or (
            self.op2.has_permission(request, view)
            and self.op2.has_object_permission(request, view, obj)
        ) or (
            self.op3.has_permission(request, view)
            and self.op3.has_object_permission(request, view, obj)
        )
