from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from .models import *
from.sessioncart import *


def cartCount(request):
    if request.user.is_authenticated:
        user = request.user
        customer, create = Customer.objects.get_or_create(account=user)

        cart, created = Cart.objects.get_or_create(customer=customer, completed=False)

        products = cart.orderproduct_set.all()

        payments = Payment.objects.filter(customer=customer)
        if payments:
            payment = list(payments)[0]
        else:
            payment = 0
        
        basket = CartSession(request)
        

        orderPro = OrderProduct.objects.filter(customer=customer, bought=True).order_by('-id')

        saved_products = SavedProduct.objects.filter(customer=customer).order_by('-id')
        
        if ShippingAddress:
            shipping, create = ShippingAddress.objects.get_or_create(customer=customer)

        category = Category.objects.all().order_by('name')

        context = {'customer_order_products': products, 'shipping': shipping, 'cart': cart, 'saved_products': saved_products, 'category': category, 'customer': customer, 'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY, 'orderPro': orderPro, 'basket': basket}

    else:
        products = []
        cart = 0
        count = 0
        orders = 0
        context = {'customer_order_products': None, 'shipping': None, 'cart': cart, 'saved_products': None}
    
    return context