from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('upi-qr/', views.upi_qr_view, name='upi_qr'),
    path('order/success/<int:pk>/', views.order_success_view, name='order_success'),
    path('orders/', views.my_orders_view, name='my_orders'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('buy-now/<int:pk>/', views.buy_now, name='buy_now'),
]
