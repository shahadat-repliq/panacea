from django.urls import path

from delivery.rest.views.delivery import (
    DeliveryViewSet,
    DeliveryAssignViewSet,
    DeliveryDetailViewSet,
    DeliveryUserViewSet,
    CreateDeliveryUserViewSet,
)

urlpatterns = [
    path("", DeliveryViewSet.as_view(), name="delivery"),
    path("/user", DeliveryUserViewSet.as_view(), name="delivery-user"),
    path("/add", CreateDeliveryUserViewSet.as_view(), name="delivery-add-user"),
    path(
        "/<uuid:delivery_id>", DeliveryDetailViewSet.as_view(), name="delivery-detail"
    ),
    path("/assign", DeliveryAssignViewSet.as_view(), name="delivery-assign"),
]
