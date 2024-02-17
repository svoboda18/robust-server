from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ApplyMentorshipView, GetIdeaAudienceView, StartupViewSet

startups = DefaultRouter()
startups.register(r'', StartupViewSet, basename='startup')

urlpatterns = [
    *startups.urls,
    path('mentor', ApplyMentorshipView.as_view()),
    path('audience', GetIdeaAudienceView.as_view())
]