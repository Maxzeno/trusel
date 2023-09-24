'''











class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance





class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'password', 'username', 'is_active', 'email_confirmed',
                  'role', 'profession']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        regular_user = RegularUser.objects.filter(user=instance)

        representation['profession'] = regular_user.profession
        return representation







from rest_framework import serializers
from .models import Model1, Model2

class CombinedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model1
        fields = '__all__'  # Include all fields from Model1
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get the fields from Model2 and add them to the serializer
        model2_fields = [field.name for field in Model2._meta.get_fields()]
        
        for field_name in model2_fields:
            self.fields[field_name] = serializers.CharField(source=f'model2.{field_name}')

















   def get_serializer_class(self):
        # if hasattr(self.request, 'user') and self.request.user.is_authenticated:
        #     if self.request.user.is_regular_user:
        #         serializer = serializers.UserRegularUser
        #     elif self.request.user.is_counselor:
        #         serializer = serializers.UserCounselor
        #     elif self.request.user.is_moderator:
        #         serializer = serializers.UserModerator
        #     else:
        #         serializer = serializers.NoneUser
        #     return serializer
        return serializers.NoneUser
    

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
'''
