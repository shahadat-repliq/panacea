from django.urls import path

from order.rest.views.order import OrderViewSet

urlpatterns = [
    path("", OrderViewSet.as_view(), name="order-list"),
]
