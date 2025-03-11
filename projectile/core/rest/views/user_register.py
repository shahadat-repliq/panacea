from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.rest.serializers.user_serializer import UserRegisterSerializer
from shared.serializers import UserSerializer

User = get_user_model()


class UserRegisterViewSet(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserViewSet(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
