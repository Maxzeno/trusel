from rest_framework import serializers
from api import models

# LIST, RETRIEVE


class RegularUser(serializers.ModelSerializer):
    class Meta:
        model = models.RegularUser
        fields = ['profession']


class Counselor(serializers.ModelSerializer):
    class Meta:
        model = models.Counselor
        fields = ['qualification', 'description']


class Moderator(serializers.ModelSerializer):
    class Meta:
        model = models.Moderator
        fields = ['qualification']


class UserSerializer(serializers.ModelSerializer):
    user = None

    class Meta:
        model = models.User
        fields = ['id', 'email', 'username', 'is_active',
                  'role', 'user']


class NoneUser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'username',
                  'is_active', 'role']


class UserRegularUser(UserSerializer):
    user = RegularUser(source='regularuser')


class UserModerator(UserSerializer):
    user = Moderator(source='moderator')


class UserCounselor(UserSerializer):
    user = Counselor(source='counselor')

# CREATE


class UserPostSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(min_length=8, max_length=100)

    def validate_email(self, value):
        if models.User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(
                "This email address is already in use.")
        return value


class UserPostRegularUser(UserPostSerializer):
    profession = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        profession = validated_data.pop('profession', '')

        user = models.User.objects.create(**validated_data)
        if profession:
            models.RegularUser.objects.create(
                profession=profession, user=user)
        return user

    def update(self, instance, validated_data):
        instance.regularuser.profession = validated_data.pop('profession', '')
        instance.regularuser.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserPostCounselor(UserPostSerializer):
    qualification = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        qualification = validated_data.pop('qualification', '')
        description = validated_data.pop('description', '')

        user = models.User.objects.create(**validated_data)
        if qualification or description:
            models.Counselor.objects.create(
                qualification=qualification, description=description, user=user)
        return user

    def update(self, instance, validated_data):
        instance.counselor.qualification = validated_data.pop(
            'qualification', '')
        instance.counselor.description = validated_data.pop('description', '')
        instance.counselor.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserPostModerator(UserPostSerializer):
    qualification = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        qualification = validated_data.pop('qualification', '')

        user = models.User.objects.create(**validated_data)
        if qualification:
            models.Moderator.objects.create(
                qualification=qualification, user=user)
        return user

    def update(self, instance, validated_data):
        instance.moderator.qualification = validated_data.pop(
            'qualification', '')
        instance.moderator.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# UPDATE, PARTIAL_UPDATE

class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)


class UserUpdateRegularUser(UserUpdateSerializer):
    profession = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        instance.regularuser.profession = validated_data.pop(
            'profession', None) or instance.regularuser.profession
        instance.regularuser.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserUpdateCounselor(UserUpdateSerializer):
    qualification = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        instance.counselor.qualification = validated_data.pop(
            'qualification', None) or instance.counselor.qualification
        instance.counselor.description = validated_data.pop(
            'description', None) or instance.counselor.description
        instance.counselor.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserUpdateModerator(UserUpdateSerializer):
    qualification = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        instance.moderator.qualification = validated_data.pop(
            'qualification', None) or instance.moderator.qualification
        instance.moderator.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
