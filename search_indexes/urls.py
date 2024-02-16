from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StartupViewSet

startups = DefaultRouter()
startups.register(r'startups', StartupViewSet, basename='search_startupdocument')

urlpatterns = startups.urls