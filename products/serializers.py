from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "active", "categories", "default", "productimage_set",
                  "variation_set"]
