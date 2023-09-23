
from api import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import generics, reverse, status, mixins, views
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
class UserView(views.APIView):
    permission_classes = [IsAuthenticated]

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
        return Response(data)


@extend_schema(tags=['Auth'])
class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = serializers.ForgotPasswordSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = get_user_model().objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.get_host()}{reverse.reverse('password_reset', kwargs={'uid': uid, 'token': token})}"

            # html_body = get_template('login/template_confirm_email.html').render({'confirmation_email': link, 'base_url': base_url})
            try:
                msg = EmailMultiAlternatives(
                    'Password Reset',
                    f'Click the following link to reset your password: {reset_url}',
                    config('EMAIL_HOST_USER'),
                    [email]
                )
                # msg.attach_alternative(html_body, "text/html")
                msg.send()
            except ConnectionRefusedError as e:
                return Response({'message': 'An error accurred while tring to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'If an account with this email exists, a password reset email has been sent.'})


@extend_schema(tags=['Auth'])
class PasswordResetView(UpdateOnlyAPIView):
    serializer_class = serializers.PasswordResetSerializer
    authentication_classes = ()
    permission_classes = ()

    def update(self, request, *args, **kwargs):
        token = kwargs.get('token')
        uid = kwargs.get('uid')
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.filter(pk=uid).first()

        if user and default_token_generator.check_token(user, token):
            password = request.data.get('password')
            password_again = request.data.get('password_again')
            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)
            if password != password_again:
                return Response({'message': 'password and repeat does not match'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
