from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from fcm.views import FCMDeviceView
urlpatterns = [
    re_path(r'^$', FCMDeviceView.as_view()),
]