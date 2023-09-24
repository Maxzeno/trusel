from django.urls import path, include

from api import views
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()

router.register('regular-user', views.RegularUser,
                basename='regular_user')
router.register('counselor', views.Counselor,
                basename='counselor')
router.register('moderator', views.Moderator,
                basename='moderator')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/blacklist/', views.MyTokenBlacklistView.as_view(),
         name='token_blacklist'),

    path('get-auth-user/', views.UserView.as_view(),
         name='get_auth_user'),

    path('verify-otp/', views.VerifyOTP.as_view(),
         name='verify_otp'),

    path('confirm-email/', views.ConfirmEmail.as_view(),
         name='confirm_email'),

    path('forgot-password/', views.ForgotPasswordView.as_view(),
         name='forgot_password'),

    path('password-reset/',
         views.PasswordResetView.as_view(), name='password_reset'),


    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
