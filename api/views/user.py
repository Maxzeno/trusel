# from rest_framework import filters
# from rest_framework import generics
from drf_spectacular.utils import extend_schema
from api.models.user import REGULAR_USER, COUNSELOR, MODERATOR
from rest_framework.viewsets import ModelViewSet
from api import serializers, models
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from api.utils.permissions_and_auth import MyAdmin, MyCounselor, MyModerator, MyOwner, MyRegularUser, MyValidUser


class BaseUser(ModelViewSet):
    serializers_get = ''
    serializers_post = ''
    serializers_update = ''

    def get_parsers(self):
        self.parser_classes.append(MultiPartParser)
        return [parser_class() for parser_class in self.parser_classes]

    def get_authenticators(self):
        if hasattr(self, 'action') and self.action == 'create':
            return []

        return [authentication_class() for authentication_class in self.authentication_classes]

    def get_permissions(self):
        if hasattr(self, 'action') and self.action == 'create':
            return []

        return [permission_class() for permission_class in self.permission_classes]

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return self.serializers_post
        if hasattr(self, 'action') and self.action in ['update', 'partial_update']:
            return self.serializers_update
        return self.serializers_get

    def create(self, request, *args, **kwargs):
        serializer = self.serializers_post(data=request.data)
        if serializer.is_valid():
            data = serializer.create(serializer.data)
            user = self.serializers_get(data)
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.serializers_update(data=request.data)
        if serializer.is_valid():
            data = serializer.update(instance, serializer.data)
            user = self.serializers_get(data)
            return Response(user.data, status=status.HTTP_200_OK)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['RegularUser'])
class RegularUser(BaseUser):
    def get_permissions(self):
        if hasattr(self, 'action'):
            if self.action == 'create':
                self.permission_classes = []
            elif self.action in ['retrieve', 'list']:
                self.permission_classes = [MyValidUser]
            elif self.action in ['update' 'partial_update']:
                self.permission_classes = [MyAdmin | MyModerator |
                                           MyRegularUser & MyOwner]
            elif self.action in ['destroy']:
                self.permission_classes = [MyAdmin | MyRegularUser & MyOwner]
            else:
                self.permission_classes = []

        return [permission_class() for permission_class in self.permission_classes]

    serializers_get = serializers.UserRegularUser
    serializers_post = serializers.UserPostRegularUser
    serializers_update = serializers.UserUpdateRegularUser

    queryset = models.User.objects.filter(role=REGULAR_USER)


@extend_schema(tags=['Counselor'])
class Counselor(BaseUser):
    def get_permissions(self):
        if hasattr(self, 'action'):
            if self.action == 'create':
                self.permission_classes = []
            elif self.action in ['retrieve', 'list']:
                self.permission_classes = [MyValidUser]
            elif self.action in ['update' 'partial_update']:
                self.permission_classes = [MyAdmin | MyModerator |
                                           MyCounselor & MyOwner]
            elif self.action in ['destroy']:
                self.permission_classes = [MyAdmin | MyCounselor & MyOwner]
            else:
                self.permission_classes = []

        return [permission_class() for permission_class in self.permission_classes]

    serializers_get = serializers.UserCounselor
    serializers_post = serializers.UserPostCounselor
    serializers_update = serializers.UserUpdateCounselor

    queryset = models.User.objects.filter(role=COUNSELOR)


@extend_schema(tags=['Moderator'])
class Moderator(BaseUser):
    def get_permissions(self):
        if hasattr(self, 'action'):
            if self.action == 'create':
                self.permission_classes = [MyAdmin]
            elif self.action == 'retrieve':
                self.permission_classes = [MyAdmin | MyCounselor & MyOwner]
            elif self.action == 'list':
                self.permission_classes = [MyAdmin]
            elif self.action in ['update' 'partial_update', 'destroy']:
                self.permission_classes = [MyAdmin | MyModerator & MyOwner]
            else:
                self.permission_classes = []

        return [permission_class() for permission_class in self.permission_classes]

    serializers_get = serializers.UserModerator
    serializers_post = serializers.UserPostModerator
    serializers_update = serializers.UserUpdateModerator

    queryset = models.User.objects.filter(role=MODERATOR)

    def get_authenticators(self):
        return [authentication_class() for authentication_class in self.authentication_classes]
