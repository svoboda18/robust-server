import json
import numpy as np
import pandas as pd
from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from fcm_django.models import FCMDevice
import tensorflow as tf

from startup.models import Startup
from firebase_admin.messaging import Notification, Message

from startup.serializers import StartupIDSerializer, StartupSerializer,  StartupAiSerializer

from settings import BASE_DIR
from startup.models import Startup

# import google.generativeai as genai

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
class AiConsulting(APIView):
    serializer_class = StartupAiSerializer
    permission_classes = (AllowAny,)
    def post(self,request):    
        model = tf.keras.models.load_model('C:/Users/acer/Desktop/CoEscape/my_saved_model')           
        # try:
        # serializer = self.serializer_class(data=request.data) 
        # serializer.is_valid()
        #     print(serializer.is_valid())
        #     print('serializer is validated')
        # print(serializer.validated_data)
        #     df = pd.DataFrame(data)                    
        
        # except Exception as e:
        #     print('looooooooooool')
        #     return Response(e)    
        json_data = request.body.decode('utf-8')
        json_data_dict = json.loads(json_data)
        json_data_dict['labels'] = 1 if (json_data_dict.get('labels')) else 0
        json_data_dict['category_code'] = 1 if (json_data_dict.get('category_code')) else 0

        for key in json_data_dict:
            if (isinstance(json_data_dict[key], bool)):  json_data_dict[key] = 1 if json_data_dict[key] else 0
        id = json_data_dict.pop('startup')
        print(json_data_dict)
        numpy_array = np.array(list(json_data_dict.values()))
        numpy_array = numpy_array.reshape(1, -1)

        print(numpy_array)

        df = pd.DataFrame.from_records([json_data_dict.values()])
        result = model.predict(numpy_array)
        startup = Startup.objects.all().filter(id = id ).first()
        startup.status = 'ai-approved' if result else 'closed'
        startup.save()

        return Response({startup.status})  

# example_data = np.array([0.53000151, 1.29700817, -1.35536136, -0.63177276, -1.05000483, -0.83929656,
        #                                 -1.12828503, -0.78160911, -0.19364912, -0.64589369, -0.64374518, -1.02835207,
        #                                 -0.36305674, -0.3086067, -0.23608834, 1.83066965, -1.58658548, -0.46871843,
        #                                 -0.42133542, -0.29637449, -0.29326332, -0.26075538, -0.23608834, -0.16466098,
        #                                 -0.19245009, -0.06841189, 1.43759058, -0.67846699, 1.71782428, -1.02516116,
        #                                 -0.79396458, -0.53425569, -0.32346749, -0.99218086, -1.97889629])
        # example_data = example_data.reshape(1, -1)            
        # print( model.predict(example_data)) 



