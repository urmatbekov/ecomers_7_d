from django.contrib import admin
from products.models import Product, Variation,ProductImage, Category,ProductFeatured
# Register your models here.

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price')
    inlines = [
        VariationInline,
        ProductImageInline,
    ]
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('title','price')
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)
