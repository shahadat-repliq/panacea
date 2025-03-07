from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from core.rest.serializers.user_serializer import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
