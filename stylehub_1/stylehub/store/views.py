import base64
from io import BytesIO

import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from urllib.parse import quote
from .models import Product, Cart, Order, OrderItem


def home_view(request):
    categories = ['women', 'men', 'kids', 'boys', 'shoes']
    category_products = {}
    for cat in categories:
        category_products[cat] = Product.objects.filter(category=cat, is_active=True)[:8]
    return render(request, 'store/home.html', {'category_products': category_products})


def category_view(request, category):
    products = Product.objects.filter(category=category, is_active=True)
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    return render(request, 'store/category.html', {
        'products': products, 'category': category, 'sort': sort
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})


def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query, is_active=True) if query else []
    return render(request, 'store/search.html', {'products': products, 'query': query})


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
def remove_from_cart(request, pk):
    Cart.objects.filter(user=request.user, product_id=pk).delete()
    return redirect('cart')


@login_required
def update_cart(request, pk):
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        Cart.objects.filter(user=request.user, product_id=pk).update(quantity=qty)
    else:
        Cart.objects.filter(user=request.user, product_id=pk).delete()
    return redirect('cart')


def generate_qr_data_uri(data, box_size=8, border=2):
    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}'


@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in cart_items)

    payment_methods = [
        ('cod', '💵 Cash on Delivery'),
        ('upi', '📱 UPI (GPay/PhonePe/Paytm)'),
        ('card', '💳 Credit/Debit Card'),
    ]
    upi_vpa = 'rohitraj66295@okhdfcbank'
    upi_payload = f"upi://pay?pa={quote(upi_vpa)}&pn={quote('Rohit Raj')}&am={quote(str(total))}&cu=INR&tn={quote('StyleHub order')}"
    upi_qr_data = generate_qr_data_uri(upi_payload)

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not address or not phone:
            messages.error(request, 'Address and phone are required.')
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'payment_methods': payment_methods,
                'upi_vpa': upi_vpa,
            })
        order = Order.objects.create(
            user=request.user, total_price=total, address=address, phone=phone
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity, price=item.product.price
            )
        cart_items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success', pk=order.pk)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'payment_methods': payment_methods,
        'upi_vpa': upi_vpa,
        'upi_qr_data': upi_qr_data,
    })


@login_required
def upi_qr_view(request):
    upi_vpa = 'rohitraj66295@okhdfcbank'
    upi_payload = f"upi://pay?pa={quote(upi_vpa)}&pn={quote('Rohit Raj')}&cu=INR"
    upi_qr_data = generate_qr_data_uri(upi_payload, box_size=10)
    return render(request, 'store/upi_qr.html', {
        'upi_vpa': upi_vpa,
        'upi_qr_data': upi_qr_data,
    })


@login_required
def order_success_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Cart.objects.filter(user=request.user).delete()
    Cart.objects.create(user=request.user, product=product, quantity=1)
    return redirect('checkout')
