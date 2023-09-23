from rest_framework import serializers
from api import models


class RegularUser(serializers.ModelSerializer):
    class Meta:
        model = models.RegularUser
        fields = ['profession']


class Counselor(serializers.ModelSerializer):
    class Meta:
        model = models.Counselor
        fields = ['qualification']


class Moderator(serializers.ModelSerializer):
    class Meta:
        model = models.Moderator
        fields = ['qualification']


class UserSerializer(serializers.ModelSerializer):
    user = None

    class Meta:
        model = models.User
        fields = ['id', 'email', 'password', 'username', 'is_active', 'email_confirmed',
                  'role', 'user']
        extra_kwargs = {'password': {'write_only': True}}


class UserRegularUser(UserSerializer):
    user = RegularUser(source='regularuser')


class UserModerator(UserSerializer):
    user = Moderator(source='moderator')


class UserCounselor(UserSerializer):
    user = Counselor(source='counselor')

# POST


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'password', 'username', 'is_active', 'email_confirmed',
                  'role', 'regularuser.profession']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        regular_user = RegularUser.objects.filter(user=instance)

        representation['profession'] = regular_user.profession
        return representation
