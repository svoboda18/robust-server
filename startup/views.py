from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from rest_framework.response import Response
from fcm_django.models import FCMDevice

from startup.models import Startup
from firebase_admin.messaging import Notification, Message

from startup.serializers import StartupIDSerializer, StartupSerializer
from startup.models import Startup

import google.generativeai as genai

class StartupViewSet(ModelViewSet):
    serializer_class = StartupSerializer

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

class GetIdeaAudienceView(APIView):    
    def post(self, request, *args, **kwargs):
        serialized = StartupIDSerializer(data=request.data)

        if not serialized.is_valid():
            return Response({"error": serialized.errors}, status=403)

        id = serialized.validated_data.get('startup')
        startup = Startup.objects.all().filter(id=id).first()

        genai.configure(api_key='AIzaSyCFAt_sdEkNueV2m1AEcHR_-BRAqA7eeaE')
        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(f"give, in maximuim 100 words, a most plausable audience target for a startup,  named {startup.name} described as: {startup.description}.")

        return Response({"message": response.text}, status=200)

class ApplyMentorshipView(APIView):    
    def post(self, request, *args, **kwargs):
        serialized = StartupIDSerializer(data=request.data)

        if not serialized.is_valid():
            return Response({"error": serialized.errors}, status=403)

        id = serialized.validated_data.get('startup')
        startup = Startup.objects.all().filter(id=id).first()

        if not request.user.is_mentor:
            return Response({"error": "You are not allowed to mentor this startup"}, status=403)

        notification_title = "Mentorship Recieved"
        notification_body = f"{request.user.first_name + request.user.last_name} is now mentoring your startup!"
        
        # Send the notification
        device = FCMDevice.objects.filter(user=startup.creator).first()
        startup.mentors.add(request.user)

        if device:
            device.send_message(Message(notification=Notification(title=notification_title, body=notification_body)))
        return Response({"message": "Mentorship added"}, status=200)
