from orders.models import Order
from carts.models import Cart
class CartOrderMixin(object):
    def get_order(self,*args,**kwargs):
        new_order_id = self.request.session.get("order_id")
        cart = self.get_cart()
        if cart is None:
            return None
        if new_order_id !=None:
            new_order = Order.objects.get(id=new_order_id)
        else:
            new_order = Order.objects.create(cart=cart)
            self.request.session["order_id"] = new_order.id
        return new_order
    def get_cart(self,*args,**kwargs):
        cart_id = self.request.session.get('cart_id')
        if cart_id == None:
            return None
        cart = Cart.objects.get(id=cart_id)
        if cart.items.count() == 0:
            return None
        return cart
