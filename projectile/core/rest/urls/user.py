from django.urls import path

from core.rest.views.user_register import UserRegisterViewSet, UserViewSet

urlpatterns = [
    path("", UserViewSet.as_view(), name="user"),
    path("/register", UserRegisterViewSet.as_view(), name="register"),
]
