# from rest_framework import filters
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from api import serializers, models
from api.models.user import MODERATOR, REGULAR_USER


@extend_schema(tags=['RegularUser'])
class RegularUser(generics.ListAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = models.User.objects.filter(role=REGULAR_USER)
    serializer_class = serializers.UserRegularUser


@extend_schema(tags=['RegularUser'])
class RegularUserRD(generics.RetrieveDestroyAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = models.User.objects.filter(role=REGULAR_USER)
    serializer_class = serializers.UserRegularUser


@extend_schema(tags=['Moderator'])
class Moderator(generics.ListAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = models.User.objects.filter(role=MODERATOR)
    serializer_class = serializers.UserModerator


@extend_schema(tags=['Moderator'])
class ModeratorRD(generics.RetrieveDestroyAPIView):
    queryset = models.User.objects.filter(role=MODERATOR)
    serializer_class = serializers.UserModerator
