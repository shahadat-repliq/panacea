from django.urls import path
from product.rest.views.product import (
    ProductViewSet,
    AddProductRequestViewSet,
    ProductRequestViewSet,
    ProductRequestDetailViewSet,
)

urlpatterns = [
    path("", ProductViewSet.as_view(), name="product"),
    path("/request", AddProductRequestViewSet.as_view(), name="add-product-request"),
    path(
        "/product-request", ProductRequestViewSet.as_view(), name="product-request-list"
    ),
    path(
        "/product-request/<uuid:product_id>",
        ProductRequestDetailViewSet.as_view(),
        name="product-request-detail",
    ),
]
