from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fcm_django.models import FCMDevice

from fcm.serializers import FCMTokenSerializer

class FCMDeviceView(APIView):
    serializer_class = FCMTokenSerializer
    def post(self, request):
        serialized = FCMTokenSerializer(data=request.data)

        if serialized.is_valid():
            token = serialized.validated_data.get('token')

            try:
                device, created = FCMDevice.objects.get_or_create(user=request.user, registration_id=token)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if created:
                return Response({"message": "FCMDevice created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "FCMDevice updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

