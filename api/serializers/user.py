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
        fields = ['id', 'email', 'username', 'is_active', 'email_confirmed',
                  'role', 'user']


class UserRegularUser(UserSerializer):
    user = RegularUser(source='regularuser')


class UserModerator(UserSerializer):
    user = Moderator(source='moderator')


class UserCounselor(UserSerializer):
    user = Counselor(source='counselor')
