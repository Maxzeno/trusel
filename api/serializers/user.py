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


class NoneUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'username',
                  'is_active', 'email_confirmed', 'role']


class UserRegularUser(UserSerializer):
    user = RegularUser(source='regularuser')


class UserModerator(UserSerializer):
    user = Moderator(source='moderator')


class UserCounselor(UserSerializer):
    user = Counselor(source='counselor')

# POST


class UserPostSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(min_length=8, max_length=100)
    profession = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        profession = validated_data.pop('profession', '')
        user = models.User.objects.create(**validated_data)
        if profession:
            profession = models.RegularUser.objects.create(
                profession=profession, user=user)
        return user
