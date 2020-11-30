from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, post_save

from django.conf import settings
User = get_user_model()

from carts.models import Cart
from decimal import Decimal
# Create your models here.
import braintree

if settings.DEBUG:
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
        )
    )


class UserCheckout(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="checkout")
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True)
    f_name = models.CharField(max_length=50, null=True)
    l_name = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    braintree_id = models.CharField(blank=True, null=True, max_length=100)

    @property
    def get_braintree_id(self):
        instance = self

        if not bool(instance.braintree_id):
            result = gateway.customer.create({
                "email": instance.email,
                "id": instance.id
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        client_token = gateway.client_token.generate({
            "customer_id": customer_id,
        })
        return client_token

    def __str__(self):
        return self.email


def update_braitree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        result = gateway.customer.create({
            "email": instance.email,
        })
        if result.is_success:
            instance.braintree_id = result.customer.id
            instance.save()


post_save.connect(update_braitree_id, sender=UserCheckout)


class AddressType(models.Model):
    address_type = models.CharField(max_length=100)

    def __str__(self):
        return self.address_type


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout,on_delete=models.CASCADE)
    type = models.ForeignKey(AddressType,on_delete=models.SET_NULL,null=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return self.street

    def get_address(self):
        return '%s, %s, %s, %s' % (self.street, self.city, self.state, self.zipcode)


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Order(models.Model):
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(UserCheckout,on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL, related_name='shipping_address', null=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
    order_total = models.DecimalField(max_digits=50, decimal_places=2)
    order_id = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return str(self.cart.id)

    def mark_complated(self, order_id=None):
        self.status = 'paid'
        if order_id and not self.order_id:
            self.order_id = order_id
        self.save()


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_tatal = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_tatal


pre_save.connect(order_pre_save, sender=Order)
