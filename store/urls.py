from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('products/<int:category>/', views.get_product_by_category, name='products'),
    path('product/<int:id>/', views.product, name='product'),
    path('comment/<int:id>/', views.process_comment, name='comment'),
    path('saved_products/', views.display_saved_products, name='saved_product'),
    path('save/<int:id>/', views.add_saved_product, name='add_product'),
    path('delete/<int:id>/', views.delete_saved_product, name='delete_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateProduct/', views.updateProduct, name='updateProduct'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.editProfile, name='edit_profile'),
    path('process_shipping/', views.processShipping, name='shipping'),
    path('login/', views.LoginingUser.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.CreateUser.as_view(), name='register'),
    path('search_products/', views.searched, name='search'),
    path('password/', views.PasswordsChangeView.as_view(template_name='update-password.html'), name='password'),
    path('payment/', views.initiate_payment, name='payment'),
    path('confirm/', views.confirmPayment, name='confirm'),
    path('verify/<str:ref>/', views.verify_payment, name='verify'),
    path('contact/', views.contact, name='contact'),
    path('order_successful/', views.order_success, name='ordersuccess'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),

    path('password_reset_sent', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete')


]

