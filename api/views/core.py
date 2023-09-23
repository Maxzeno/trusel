from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from drf_spectacular.utils import extend_schema
from api import serializers, models


class AllowCreatorCreate(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.method == 'POST' or bool(request.user and request.user.is_authenticated)


class BaseModelViewSet(ModelViewSet):
	# pagination_class = LimitOffsetPagination
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]


@extend_schema(tags=['RegularUser'],
		# request=serializers.RegularUser,
        # description="Request body format: application/x-www-form-urlencoded",
        # responses=['application/json']
	)
class RegularUser(BaseModelViewSet):
	permission_classes = [AllowCreatorCreate]
	# permission_classes = []
	authentication_classes = ()

	queryset = models.RegularUser.objects.all()
	serializer_class = serializers.RegularUser
	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
	search_fields = ['user.username', 'user.email']
	# filterset_fields = ['id', 'email', 'username', 'email_confirmed', 'is_active']

	def create(self, request, *args, **kwargs):
		self.authentication_classes = ()
		return super().create(request, *args, **kwargs)
