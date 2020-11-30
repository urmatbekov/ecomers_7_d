from django.db.models.signals import post_save
from django.utils.text import slugify
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe


class ProductManager(models.Manager):
    def get_related(self, instance):
        product_one = self.get_queryset().filter(categories__in=instance.categories.all())
        product_two = self.get_queryset().filter(default=instance.default)
        qs = (product_two | product_one).exclude(id=instance.id).distinct()
        return qs


# Create your models here.
class Product(models.Model):
    # TODO: Define fields here
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category',on_delete=models.SET_NULL, related_name='default_category', null=True, blank=True)

    objects = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title



    def get_html_price(self):
        if self.variation_set.first().sale_price is not None:
            html_price = '<h3 id="price">%s <small class="org-price" id="price"> %s</small></h3>' % (
            self.variation_set.first().sale_price, self.variation_set.first().price)
        else:
            html_price = '<h3 id="price">%s</h3>' % (self.variation_set.first().price)
        return mark_safe(html_price)

    def get_img_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url
        else:
            return img


class Variation(models.Model):
    # TODO: Define fields here
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_html_price(self):
        if self.sale_price is not None:
            html_price = '<h3 id="price">%s <small class="org-price" id="price"> %s</small></h3>' % (
            self.sale_price, self.price)
        else:
            html_price = '<h3 id="price">%s</h3>' % (self.price)
        return mark_safe(html_price)



    def remove_from_cart(self):
        return '%s?item=%s&delete=true' % (reverse("cart"), self.id)

    def add_to_cart(self):
        return '%s?item=%s' % (reverse("cart"), self.id)

    def get_title(self):
        return '%s - %s' % (self.product.title, self.title)


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)


def image_upload_products(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    end = filename.split('.')[1]
    new_name = "%s.%s" % (slug, end)
    return "products/%s/%s" % (slug, new_name)


class ProductImage(models.Model):
    # TODO: Define fields here
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_products, )

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'

    def __str__(self):
        return str(self.product.title)


class Category(models.Model):
    # TODO: Define fields here
    title = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        return self.title




def image_upload_products_featured(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    end = filename.split('.')[1]
    new_name = "%s.%s" % (slug, end)
    return "products/%s/featured/%s" % (slug, new_name)


class ProductFeatured(models.Model):
    # TODO: Define fields here
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_products_featured, )
    title = models.CharField(blank=True, null=True, max_length=100)
    text = models.TextField(blank=True, null=True, )
    text_right = models.BooleanField(default=True)
    text_css_color = models.CharField(blank=True, null=True, max_length=20)
    show_price = models.BooleanField(default=False)
    make_image_background = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ProductFeatured'
        verbose_name_plural = 'ProductFeatureds'

    def __str__(self):
        return self.product.title
