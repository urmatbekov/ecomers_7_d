from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
