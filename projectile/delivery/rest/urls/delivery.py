from django.urls import path

from delivery.rest.views.delivery import DeliveryViewSet

urlpatterns = [
    path("", DeliveryViewSet.as_view(), name="delivery"),
]
