from rest_framework.generics import ListAPIView

from product.models import Product
from product.rest.serializers.product import ProductSerializer


class ProductViewSet(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
