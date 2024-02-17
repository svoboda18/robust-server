<<<<<<< HEAD
from startup.models import Startup , StartupAi
=======
from fcm_django.models import FCMDevice
from startup.models import Startup
>>>>>>> origin/main

from rest_framework.serializers import Serializer, ModelSerializer, CharField, ValidationError
from rest_framework.fields import CurrentUserDefault
from firebase_admin.messaging import Notification, Message

from user.models import User

class StartupSerializer(ModelSerializer):
  def update(self, instance, validated_data):
    return super().update(instance, validated_data)

  def validate(self, attrs):
    user = self.context['request'].user
    attrs['creator'] = user
    return attrs
  
  def create(self, validated_data):
    ret = super().create(validated_data)
    
    ret.status = 'pending'

    notification_title = "New Startup"
    notification_body = f"{validated_data.get('name')} is out, Check it out!"

    devices = FCMDevice.objects.all()
    devices.send_message(Message(notification=Notification(title=notification_title, body=notification_body)))
    return ret

  class Meta:
      model = Startup
      fields = (
          '__all__'
      )

class StartupIDSerializer(Serializer):
    startup = CharField(required=True)

class StartupAiSerializer(ModelSerializer):

    def update(self, instance, validated_data):
      return super().update(instance, validated_data)
    class Meta:
        model = StartupAi
        fields = (
            '__all__'
        )        
