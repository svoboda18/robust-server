from startup.models import Startup , StartupAi

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

class StartupSerializer(ModelSerializer):

    def update(self, instance, validated_data):
      return super().update(instance, validated_data)
    class Meta:
        model = Startup
        fields = (
            '_all_'
        )

class StartupAiSerializer(ModelSerializer):

    def update(self, instance, validated_data):
      return super().update(instance, validated_data)
    class Meta:
        model = StartupAi
        fields = (
            '_all_'
        )        