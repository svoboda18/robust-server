from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from startup.serializers import StartupSerializer

class StartupViewSet(ModelViewSet):
    serializer_class = StartupSerializer