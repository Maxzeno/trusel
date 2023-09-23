
from rest_framework import generics, mixins
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import BasePermission

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)


class NoPatchPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            return False
        return True


class UpdateOnlyAPIView(mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@extend_schema(tags=['Auth'])
class MyTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Auth'])
class MyTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Auth'])
class MyTokenVerifyView(TokenVerifyView):
    pass


@extend_schema(tags=['Auth'])
class MyTokenBlacklistView(TokenBlacklistView):
    pass
