# from rest_framework import filters
# from rest_framework import generics
from drf_spectacular.utils import extend_schema
from api.models.user import REGULAR_USER, COUNSELOR, MODERATOR
from rest_framework.viewsets import ModelViewSet
from api import serializers, models


@extend_schema(tags=['RegularUser'])
class RegularUser(ModelViewSet):
    queryset = models.User.objects.filter(role=REGULAR_USER)

    def get_authenticators(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return []

        if hasattr(self, 'action') and self.action == 'create':
            return []

        return self.authentication_classes

    def get_permissions(self):
        if self.action == 'create':
            return []
        return self.permission_classes

    def get_serializer_class(self):
        return serializers.UserRegularUser

    def create(self, request, *args, **kwargs):
        # print(request, dir(request), request.data, request.POST)
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['Counselor'])
class Counselor(ModelViewSet):
    queryset = models.User.objects.filter(role=COUNSELOR)

    def get_authenticators(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return []

        if hasattr(self, 'action') and self.action == 'create':
            return []

        return self.authentication_classes

    def get_permissions(self):
        if self.action == 'create':
            return []
        return self.permission_classes

    def get_serializer_class(self):
        return serializers.UserCounselor


@extend_schema(tags=['Moderator'])
class Moderator(ModelViewSet):
    queryset = models.User.objects.filter(role=MODERATOR)
    # permission_classes = ()
    # authentication_classes = ()

    def get_serializer_class(self):
        return serializers.UserModerator
