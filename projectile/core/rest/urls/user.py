from django.urls import path

from core.rest.views.user_register import UserRegisterAPIView

urlpatterns = [path("/register", UserRegisterAPIView.as_view(), name="register")]
