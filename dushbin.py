

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'password', 'username', 'is_active', 'email_confirmed',
                  'role']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        regular_user = RegularUser.objects.filter(user=instance)

        representation['profession'] = regular_user.profession
        return representation


# middleware.py


class DynamicAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check the request path or other conditions to determine the authentication classes
        # For token-based authentication
        if request.path.startswith('/api/token/'):
            request.authenticators = [TokenAuthentication()]
        # For JWT-based authentication
        elif request.path.startswith('/api/jwt/'):
            request.authenticators = [JWTAuthentication()]
        else:
            # Default to session-based authentication
            request.authenticators = [SessionAuthentication()]

        response = self.get_response(request)
        return response


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


# class User(serializers.ModelSerializer):
#     regular_user = RegularUser(source='regularuser')
#     counselor = Counselor()
#     moderator = Moderator()

#     class Meta:
#         model = models.User
#         fields = ['id', 'email', 'username', 'is_active', 'email_confirmed',
#                   'is_staff', 'role', 'regular_user', 'counselor', 'moderator']

# def to_representation(self, instance):
#     data = super().to_representation(instance)
#     role = instance.get_role_display().lower()
#     data[role] = data.pop(f'{role}_user')  # Rename the role-specific field
#     return data


# @extend_schema(tags=['RegularUser'],
# 		# request=serializers.RegularUser,
#         # description="Request body format: application/x-www-form-urlencoded",
#         # responses=['application/json']
# 	)
# class RegularUser(BaseModelViewSet):
# 	permission_classes = [AllowCreatorCreate]
# 	# permission_classes = []
# 	authentication_classes = ()

# 	queryset = models.RegularUser.objects.all()
# 	serializer_class = serializers.RegularUser
# 	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
# 	search_fields = ['user.username', 'user.email']
# 	# filterset_fields = ['id', 'email', 'username', 'email_confirmed', 'is_active']

# 	def create(self, request, *args, **kwargs):
# 		self.authentication_classes = ()
# 		return super().create(request, *args, **kwargs)
