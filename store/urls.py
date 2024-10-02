from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index.html'),
    path('shop.html/<int:pk>/', views.shop, name='shop.html'),
    path('product.html/<int:pk>/', views.product_detail, name='product.html'),
    path('checkout.html', views.checkout, name='checkout.html'),
    path('contact.html', views.contact, name='contact.html'), 
    path('search.html', views.search_form, name='search.html'),
    path('signin.html', views.sign_in, name='signin.html'),
    path('login.html', views.log_in, name='login.html'),
    path('logout.html', views.log_out, name='logout.html'),
    path('cart.html', views.cart, name='cart.html'),

]