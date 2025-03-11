from django.urls import path
from cart.rest.views.cart import (
    CartViewSet,
    CartDetailViewSet,
    CartItemViewSet,
    CartItemDetailViewSet,
)

urlpatterns = [
    path(
        "",
        CartViewSet.as_view(),
        name="cart-list",
    ),
    path("/<uuid:uid>", CartDetailViewSet.as_view(), name="cart-details"),
    path(
        "/<uuid:uid>/cart-items",
        CartItemViewSet.as_view(),
        name="cart-items-list",
    ),
    path(
        "/<uuid:uid>/cart-items/<uuid:pk>",
        CartItemDetailViewSet.as_view(),
        name="cart-items-list",
    ),
]
