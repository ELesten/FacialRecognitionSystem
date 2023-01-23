import os
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser, UserEncoding
from .serializers import UserSerializers, PhotoSerializer
from rest_framework.response import Response
from apps.functions.train_model import train_model_by_img


class CustomUserApiView(APIView):
    serializer_class = UserSerializers

    def get(self, request):
        serializer = self.serializer_class(CustomUser.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EncodingApiView(APIView):
    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        encodings = train_model_by_img()
        UserEncoding.objects.update(
            user_encoding1=encodings[0],
            user_encoding2=encodings[1],
            user_encoding3=encodings[2])
        for f in os.listdir('media'):
            os.remove(os.path.join('media', f))
        return Response(status=status.HTTP_200_OK)

