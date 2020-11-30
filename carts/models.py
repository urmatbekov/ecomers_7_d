from django.db import models
from decimal import Decimal
from django.conf import settings
from django.db.models.signals import pre_save,post_save,post_delete
from products.models import Variation
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null = True,blank =True)
    items = models.ManyToManyField(Variation, through = 'CartItem')
    timestamp = models.DateTimeField(auto_now_add = True,auto_now = False)
    update = models.DateTimeField(auto_now_add = False,auto_now = True)
    sub_total = models.DecimalField(max_digits=50, decimal_places=2,default = 0.00)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2,default = 0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2,default = 0.00)
    tax_persent = models.DecimalField(max_digits=10, decimal_places=2,default = 0.08)
    def __str__(self):
        return str(self.id)
    def update_sub_total(self):
        items = self.cartitem_set.all()
        sub_total = 0
        for item in items:
            sub_total+=item.line_total_price
        self.sub_total = sub_total
        self.save()
def tax_total_price_total_price(sender,instance,*args,**kwargs):
    sub_total = instance.sub_total
    tax_total = sub_total*instance.tax_persent
    total = sub_total+tax_total
    instance.tax_total = '%.2f' % (tax_total)
    instance.total = '%.2f' % (total)
    instance.save
pre_save.connect(tax_total_price_total_price,sender=Cart)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    item = models.ForeignKey(Variation,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    line_total_price = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return self.item.title
    def remove(self):
        return self.item.remove_from_cart()
def sub_total_create_cart(sender,instance,*args,**kwargs):
    instance.cart.update_sub_total()
post_save.connect(sub_total_create_cart,sender=CartItem)


def line_total_price_create_cart_item(sender,instance,*args,**kwargs):
    quantity = Decimal(instance.quantity)
    price = instance.item.get_price()
    if quantity>=1:
        instance.line_total_price = Decimal(price)*quantity
        instance.save
pre_save.connect(line_total_price_create_cart_item, sender=CartItem)
post_delete.connect(sub_total_create_cart,sender=CartItem)
