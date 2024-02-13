from .models import *

class CartSession():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        cart = self.session.get('cart')
        self.cart = cart
 
    def add(self, product, orderProduct, cart):
        product_id = product.id
        cart_id = cart.id

        if product_id not in self.cart:
            self.cart[str(cart_id)] = {'total_items': cart.get_cart_items_total, 'total_amount': cart.get_cart_total}
            
            self.cart[str(product_id)] = {'product_title': product.title, 'product_price': product.price, 'product_quantity': orderProduct.quantity}
            
        self.session.modified = True

    def delete(self, product):
        product_id = product.id
        
        del self.cart[str(product_id)]

        self.session.modified = True

    # def __len__(self):
    #     customer = self.request.user.customer
    #     cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
    #     items = cart.get_cart_items_total
    #     return items

    # @property
    # def get_amount(self):
    #     customer = self.request.user.customer
    #     cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
    #     total_amount = cart.get_cart_total
    #     return total_amount
