import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.views.decorators.cache import cache_page

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from .forms import *
from .sessioncart import CartSession
from .models import *

# Create your views here.


class CreateUser(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class LoginingUser(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('store')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('store')
    success_message = "Password update successful."


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='login')
def editProfile(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES
        if request.user.is_authenticated:
            user = request.user
            customer, create = Customer.objects.get_or_create(account=user)

        if image:
            customer.image = image['image']
        if data.get('first_name'):
            user.first_name = data['first_name']
        if data.get('last_name'):
            user.last_name = data['last_name']
        if data.get('email'):
            user.email = data['email']
        if data.get('contact'):
            customer.contact = data['contact']
        if data.get('address'):
            customer.address = data['address']
        if data.get('state'):
            customer.state = data['state']
        if data.get('city'):
            customer.city = data['city']
        user.save()
        customer.save()
        messages.success(request, 'Profile update successful.')
        return render(request, 'profile.html', {'success': 'Successful.'})


@login_required(login_url='login')
def searched(request):
    if request.method == 'POST':
        searched = request.POST.get('search')
        pro_title = Product.objects.filter(title__icontains=searched)
        pro_category = Category.objects.filter(name__icontains=searched)

        if not searched:
            return render(request, 'search.html', {'product_title': None,'product_category': None, 'no_search_message': 'No search item found.'})

        if pro_title or pro_category:
            return render(request, 'search.html', {'product_title': pro_title,'product_category': pro_category, 'searched': searched})
    return render(request, 'search.html', {"exist": "Item doesn't exist."})


@login_required(login_url='login')
def store(request):
    page = request.GET.get('page', 1)
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 8)
    print(request.session)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'store.html', {'products': products})


@login_required(login_url='login')
def get_product_by_category(request, category):
    page = request.GET.get('page', 1)
    product_list = Product.objects.filter(category=category)
    paginator = Paginator(product_list, 8)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'products': products})


@login_required(login_url='login')
def product(request, id):
    product = Product.objects.get(id=id)
    comments = product.comment_set.order_by('-time')[:10]
    return render(request, 'product.html', {'product': product, 'comments': comments})


@login_required(login_url='login')
def display_saved_products(request):
    return render(request, 'saved.html')


@login_required(login_url='login')
def add_saved_product(request, id):
    if request.user.is_authenticated:
        user = request.user
        customer, create = Customer.objects.get_or_create(account=user)

    product = Product.objects.get(id=id)
    saved_product, create = SavedProduct.objects.get_or_create(customer=customer, product=product)
    messages.success(request, f'{saved_product.product} was added to your saved products.')
    return HttpResponseRedirect(reverse('product', args=(product.id,)))
    

@login_required(login_url='login')
def delete_saved_product(request, id):
    saved_product = SavedProduct.objects.get(id=id).delete()
    messages.success(request, "Product was removed successfully.")
    return redirect('saved_product')


@login_required(login_url='login')
def process_comment(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            customer, create = Customer.objects.get_or_create(account=user)

        comment = request.POST.get('comment')
        product = Product.objects.get(id=id)
        save_comment = Comment.objects.create(customer=customer, product=product, comment=comment, time=timezone.now())
        messages.success(request, 'Comment was successfully.')
        return HttpResponseRedirect(reverse('product', args=(product.id,)))


@login_required(login_url='login')
def cart(request):
    return render(request, 'cart.html')


@login_required(login_url='login')
def checkout(request):
    return render(request, 'checkout.html')


@login_required(login_url='login')
def order(request):
    return render(request, 'order.html')


@login_required(login_url='login')
def updateProduct(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    cartSession = CartSession(request)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    cart, created = Cart.objects.get_or_create(customer=customer, completed=False)

    orderProduct, created = OrderProduct.objects.get_or_create(cart=cart, product=product)

    
    if action == 'add':
        if orderProduct.quantity > 0:
            orderProduct.quantity =  (orderProduct.quantity + 1)
            messages.success(request, f"{orderProduct.product}'s quantity was increased to {orderProduct.quantity}.")
        else:
            orderProduct.quantity =  (orderProduct.quantity + 1)
            messages.success(request, f'{orderProduct.product} was added to cart.')
    elif action == 'remove':
        orderProduct.quantity = (orderProduct.quantity - 1) 

        messages.success(request, f"{orderProduct.product}'s quantity was reduced to {orderProduct.quantity}.")

    orderProduct.save()

    cartSession.add(product, orderProduct, cart)

    if orderProduct.quantity <= 0:
        orderProduct.delete()
        messages.success(request, 'Hence product was removed from cart.')
        cartSession.delete(product)

    return JsonResponse('Product was added', safe=False)


@login_required(login_url='login')
def processShipping(request):
    if request.method == 'POST':
        data = request.POST
        if request.user.is_authenticated:
            user = request.user
        customer, create = Customer.objects.get_or_create(account=user)
        address = data['address']
        city = data['city']
        state = data['state']
        ship = ShippingAddress.objects.get(customer=customer)
        ship.address = address
        ship.city = city
        ship.state = state
        ship.delivery_date = timezone.now() + timedelta(days=3)
        ship.save()
        messages.success(request, 'Shipping Information updated.')
    return redirect('checkout')


@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        send_mail(
            f'Message from {name}',#
            f'Email: {email}\n\n \
        Subject: {subject}\n\n \
        Message: {message}', # message
        email, # from email
            ['adeyemideji2@gmail.com'] # to emails
        )

        contact = Enquiry.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'Your request was sent successfully.')
        return redirect('contact')
    return render(request, 'contact.html')


@login_required(login_url='login')
def initiate_payment(request):
    if request.method == 'POST':
        data = request.POST
        amount = data.get('amount')
        if request.user.is_authenticated:
            user = request.user
            customer, created = Customer.objects.get_or_create(account=user)
        payment = Payment.objects.create(customer=customer, amount=amount)
        return redirect('confirm')


@login_required(login_url='login')
def confirmPayment(request):
    return render(request, 'confirmpayment.html')


@login_required(login_url='login')
def verify_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.get(account=user)
            cart = Cart.objects.get(customer=customer, completed=False)
            cart.order_date = datetime.now()
            cart.completed = True
            cart.transaction_id = ref
            cart.save()
            products = cart.orderproduct_set.all()
            for product in products:
                product.customer = customer
                product.bought = True
                product.transaction_id = ref
                product_order_date = datetime.now()
                product.save();
        messages.success(request, 'Payment verification Successful.')
    else:
        messages.error(request, "Verification Failed.")
    return redirect('ordersuccess')


@login_required(login_url='login')
def order_success(request):
    return render(request, 'ordersuccess.html')





# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm = request.POST.get('confirm_password')
#         users = User.objects.all()

#         try:    
        
#             if not username in users:
#                 if password == confirm:
#                     user = User.objects.create_user(username=username, email=email, password=password)
#                     customer = Customer.objects.create(user=user)
#                     return redirect('login')
#                 else:
#                     return render(request, 'register.html', {"error": "Password don't match.", 'username': username, 'email': email, 'username_exist': "Username already exist."})    

#         except IntegrityError:
            
#             return render(request, 'register.html', {'username_exist': "Username already exist.", 'username': username, 'email': email})
        
#     return render(request, 'register.html')


# def get_server_side_cookie(request, cookie, default_val=None):
#     val = request.session.get(cookie)
#     if not val:
#         val = default_val
#     return val

# def visitor_cookie_handler(request):
#     visits = int(get_server_side_cookie(request, 'visits', '1'))
#     last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

#     if (datetime.now() - last_visit_time).seconds > 0:
#         visits += 1
#         request.session['last_visit'] = str(datetime.now())
#     else:
#         visits = 1
#         request.session['last_visit'] = last_visit_cookie
#     request.session['visits'] = visits