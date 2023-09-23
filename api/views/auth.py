
from django.shortcuts import get_object_or_404
from api import serializers
from rest_framework.permissions import BasePermission
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, status, mixins
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from rest_framework import generics, mixins
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
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
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = {'token': serializer.validated_data['access']}
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
class MyTokenBlacklistView(TokenBlacklistView):
    pass


@extend_schema(tags=['Auth'])
class UserView(generics.GenericAPIView):

    def get_serializer_class(self):
        return serializers.NoneUser

    def get(self, request):
        if request.user.is_regular_user:
            serializer = serializers.UserRegularUser(request.user)
        elif request.user.is_counselor:
            serializer = serializers.UserCounselor(request.user)
        elif request.user.is_moderator:
            serializer = serializers.UserModerator(request.user)
        else:
            serializer = serializers.NoneUser(request.user)
        data = serializer.data
        data['token'] = request.META.get('HTTP_AUTHORIZATION', '').split()[-1]
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = serializers.ForgotPasswordSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        user = get_user_model().objects.filter(email=email).first()

        if user:
            # html_body = get_template('login/template_confirm_email.html').render({'confirmation_email': link, 'base_url': base_url})
            try:
                msg = EmailMultiAlternatives(
                    'Password Reset OTP Code',
                    f'OTP code use it to confirm your email: {user.generate_otp()}',
                    config('EMAIL_HOST_USER'),
                    [email]
                )
                # msg.attach_alternative(html_body, "text/html")
                msg.send()
                return Response({'detail': 'If an account with this email exists, a password reset email has been sent.'}, status=status.HTTP_200_OK)
            except ConnectionRefusedError as e:
                return Response({'detail': 'An error accurred while tring to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': 'If an account with this email exists, a password reset email has been sent.'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
class VerifyOTP(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.VerifyOTPSerializer

    def create(self, request):
        email = request.data.get('email', '').strip()
        opt = request.data.get('otp', '').strip()
        user = get_object_or_404(get_user_model(), email=email)
        status_code = status.HTTP_404_NOT_FOUND
        data = {'detail': user.verify_otp(opt, verify_and_clear=False)}
        if data['detail']:
            status_code = status.HTTP_200_OK
        return Response(data, status=status_code)


@extend_schema(tags=['Auth'])
class PasswordResetView(UpdateOnlyAPIView):
    serializer_class = serializers.PasswordResetSerializer
    authentication_classes = ()
    permission_classes = ()

    def update(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        opt = request.data.get('otp', '').strip()
        user = get_object_or_404(get_user_model(), email=email)

        if user and user.verify_otp(opt, verify_and_clear=False):
            password = request.data.get('password', '').strip()
            password_again = request.data.get('password_again', '').strip()
            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                return Response({'detail': e.messages[-1]}, status=status.HTTP_400_BAD_REQUEST)
            if password != password_again:
                return Response({'detail': 'password and repeat does not match'}, status=status.HTTP_400_BAD_REQUEST)
            user.verify_otp(opt, verify_and_clear=True)
            print('the pass', password)
            print(user.password)
            user.password = password
            print(user.password)
            user.save()
            print(user.password)

            return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
