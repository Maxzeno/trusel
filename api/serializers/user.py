from rest_framework import serializers
from api import models

class User(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ('groups', 'user_permissions')


class RegularUser(serializers.ModelSerializer):
    user = User()
    class Meta:
        model = models.RegularUser
        fields = '__all__'
