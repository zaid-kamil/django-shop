from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/all/', views.all_products, name='listing'),
    path('products/<slug:slug>/', views.product_detail, name='detail'),
    # search urls
    path('search/', views.search, name='search'),
    # category urls
    path('categories/all/', views.all_categories, name='all_categories'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    # cart urls
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pid>/', views.remove_from_cart, name='remove_from_cart'),
    # order urls
    path('orders/all/', views.all_orders, name='all_orders'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:oid>/', views.order_detail, name='order_detail'),
    # checkout urls
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancelled/', views.checkout_cancelled, name='checkout_cancelled'),
    # payment urls
    path('payment/process/', views.payment_process, name='payment_process'),
    
]