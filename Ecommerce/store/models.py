from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
import secrets
from .paystack import PayStack

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager() 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    

class Customer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    contact = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.account.username

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class CategoryType(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_type = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categorie'

Shoe_sizes = (
    ('40', '40'),
    ('41', '41'),
    ('38', '38'),
    ('42', '42'),
    ('39', '39'),
)

Size = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large')
)

class Product(models.Model):
    title = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    shoe_sizes = models.CharField(choices=Shoe_sizes, max_length=2, null=True, blank=True)
    size = models.CharField(choices=Size, max_length=2, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    price = models.IntegerField()
    image1 = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True)
    image3 = models.ImageField(blank=True)
    image4 = models.ImageField(blank=True)

    def __str__(self):
        return str(self.title)

    @property
    def imageUrl(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url

    @property
    def imageUrl2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def imageUrl3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url

    @property
    def imageUrl4(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.customer.account.username)


    @property
    def get_cart_total(self):
        orderProducts = self.orderproduct_set.all()
        total = sum([int(item.get_item_total) for item in orderProducts])
        return total

    @property
    def get_cart_items_total(self):
        orderProducts = self.orderproduct_set.all()
        total = sum([int(item.quantity) for item in orderProducts])
        return total


class OrderProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    bought = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        ordering = ['-id']

    @property
    def get_item_total(self):
        total = self.product.price * self.quantity
        return total


class SavedProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.account.username


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = 'Shipping Addres'


class Contact(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(default='admin@gmail.com')
    phone1 = models.CharField(max_length=200, null=True, blank=True)
    phone2 = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.addr;ess


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.customer.account.username

    
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(default=0)
    ref = models.CharField(max_length=200, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(20)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        result = {'amount': self.amount}
        if status:
            if result['amount'] == self.amount:
                self.verified = True
                self.save()
        if self.verified:
            return True
        return False


class Enquiry(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=30, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name