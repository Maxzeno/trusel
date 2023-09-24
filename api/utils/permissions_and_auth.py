from rest_framework.permissions import BasePermission


class MyValidUser(BasePermission):
    code = 403

    def has_permission(self, request, view):
        if request.user:
            if not request.user.is_active:
                self.message = 'user is not active'
                return False
            if not request.user.email_confirmed:
                self.message = 'Email not confirmed'
                return False
            if request.user.is_authenticated:
                self.code = 200
                self.message = "Successfull"
                return True

        self.code = 401
        self.message = "Not Authorized"
        return False


class MyAdmin(BasePermission):
    def has_permission(self, request, view):
        return MyValidUser().has_permission(request, view) and request.user.is_staff and request.user.is_superuser


class MyModerator(BasePermission):
    def has_permission(self, request, view):
        return MyValidUser().has_permission(request, view) and request.user.is_moderator


class MyCounselor(BasePermission):
    def has_permission(self, request, view):
        return MyValidUser().has_permission(request, view) and request.user.is_counselor


class MyRegularUser(BasePermission):
    def has_permission(self, request, view):
        print(MyValidUser().has_permission(request, view))
        return MyValidUser().has_permission(request, view) and request.user.is_regular_user


class MyOwner(BasePermission):
    def has_permission(self, request, view):
        print(view.kwargs)
        try:
            obj = view.get_queryset().get(pk=view.kwargs['pk'])
        except Exception as e:
            return False
        return obj == request.user
