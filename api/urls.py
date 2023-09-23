from django.urls import path, include

from api import views
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()

# router.register('regular_user', views.RegularUser, basename='regular_user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/blacklist/', views.MyTokenBlacklistView.as_view(),
         name='token_blacklist'),
    path('token/refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.MyTokenVerifyView.as_view(), name='token_verify'),
    # path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    # path('password-reset/<str:uid>/<str:token>/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('user/', views.User.as_view(), name='user_list'),
    # path('user/<str:id>', views.UserDetails.as_view(), name='user_details'),
    path('regular-user', views.RegularUser.as_view(), name='regular_user'),
    path('regular-user/<str:pk>', views.RegularUserRD.as_view(),
         name='regular_user_details'),
    path('moderator', views.Moderator.as_view(), name='moderator'),
    path('moderator/<str:pk>', views.ModeratorRD.as_view(),
         name='moderator_details'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
