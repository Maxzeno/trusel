# from rest_framework import filters
# from rest_framework import generics
from drf_spectacular.utils import extend_schema
from api.models.user import REGULAR_USER, COUNSELOR, MODERATOR
from rest_framework.viewsets import ModelViewSet
from api import serializers, models
from rest_framework.parsers import MultiPartParser


@extend_schema(tags=['RegularUser'])
class RegularUser(ModelViewSet):
    queryset = models.User.objects.filter(role=REGULAR_USER)

    def get_parsers(self):
        self.parser_classes.append(MultiPartParser)
        return [parser_class() for parser_class in self.parser_classes]

    def get_authenticators(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return []

        if hasattr(self, 'action') and self.action == 'create':
            return []

        return [authentication_class() for authentication_class in self.authentication_classes]

    def get_permissions(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return []

        if hasattr(self, 'action') and self.action == 'create':
            return []
        return [permission_class() for permission_class in self.permission_classes]

    def get_serializer_class(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return serializers.UserPostSerializer

        if hasattr(self, 'action') and self.action == 'create':
            return serializers.UserPostSerializer
        return serializers.UserRegularUser

    def create(self, request, *args, **kwargs):
        serialize = serializers.UserPostSerializer(data=request.data)
        print(dir(serialize), serialize.data, dir(serialize.is_valid))
        if serialize.is_valid():
            print('hoooooo')
            serialize.save()
        return serialize


@extend_schema(tags=['Counselor'])
class Counselor(ModelViewSet):
    queryset = models.User.objects.filter(role=COUNSELOR)

    def get_parsers(self):
        self.parser_classes.append(MultiPartParser)
        return [parser_class() for parser_class in self.parser_classes]

    def get_authenticators(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return []

        if hasattr(self, 'action') and self.action == 'create':
            return []

        return [authentication_class() for authentication_class in self.authentication_classes]

    def get_permissions(self):
        if hasattr(self.request, 'method') and self.request.method == 'POST':
            return []

        if hasattr(self, 'action') and self.action == 'create':
            return []
        return [permission_class() for permission_class in self.permission_classes]

    def get_serializer_class(self):
        return serializers.UserCounselor


@extend_schema(tags=['Moderator'])
class Moderator(ModelViewSet):
    queryset = models.User.objects.filter(role=MODERATOR)

    def get_parsers(self):
        self.parser_classes.append(MultiPartParser)
        return [parser_class() for parser_class in self.parser_classes]

    def get_serializer_class(self):
        return serializers.UserModerator
