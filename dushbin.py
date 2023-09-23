

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
