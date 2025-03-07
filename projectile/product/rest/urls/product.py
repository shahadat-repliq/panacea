from django.urls import path
from product.rest.views.product import ProductViewSet

urlpatterns = [
    path("", ProductViewSet.as_view(), name="product"),
]
