# from rest_framework import filters
# from rest_framework import generics
from drf_spectacular.utils import extend_schema
from api.models.user import REGULAR_USER  # MODERATOR
from rest_framework.viewsets import ModelViewSet
from api import serializers, models


@extend_schema(tags=['RegularUser'])
class RegularUserViewSet(ModelViewSet):
    queryset = models.User.objects.filter(role=REGULAR_USER)

    def get_authenticators(self):
        if self.action == 'create':
            return []
        return self.authentication_classes

    def get_permissions(self):
        # if self.action == 'create':
        #     return []
        return self.permission_classes

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserPostSerializer

        return serializers.UserRegularUser


# @extend_schema(tags=['RegularUser'])
# class RegularUser(generics.ListCreateAPIView):
#     permission_classes = ()
#     authentication_classes = ()
#     queryset = models.User.objects.filter(role=REGULAR_USER)
#     serializer_class = serializers.UserRegularUser


# @extend_schema(tags=['RegularUser'])
# class RegularUserRD(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.User.objects.filter(role=REGULAR_USER)
#     serializer_class = serializers.UserRegularUser


# @extend_schema(tags=['Moderator'])
# class Moderator(generics.ListCreateAPIView):
#     permission_classes = ()
#     authentication_classes = ()
#     queryset = models.User.objects.filter(role=MODERATOR)
#     serializer_class = serializers.UserModerator


# @extend_schema(tags=['Moderator'])
# class ModeratorRD(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.User.objects.filter(role=MODERATOR)
#     serializer_class = serializers.UserModerator
