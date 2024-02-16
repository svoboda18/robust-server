from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import PasswordChangeAPIView, UserRegistrationAPIView, UserViewAPI

urlpatterns = [
	re_path(r'^register/?$', UserRegistrationAPIView.as_view()),
    re_path(r'^reset/?$', PasswordChangeAPIView.as_view()),
    re_path(r'^profile/?$', UserViewAPI.as_view()),
    re_path(r'^login/?$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^login/refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
]