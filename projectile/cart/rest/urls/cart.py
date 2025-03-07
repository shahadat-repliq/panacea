from django.urls import path
from cart.rest.views.cart import CartViewSet

urlpatterns = [
    path(
        "",
        CartViewSet.as_view(),
        name="cart",
    ),
    # path("/<uuid:pk>", CartViewSet.as_view(), name="cart_item"),
]
