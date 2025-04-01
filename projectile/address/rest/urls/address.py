from django.urls import path

from address.rest.views.address import AddressViewSet

urlpatterns = [
    path("", AddressViewSet.as_view(), name="address"),
    path("/create", AddressViewSet.as_view(), name="create-address"),
]
