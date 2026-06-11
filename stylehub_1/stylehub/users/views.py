from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import SignupForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'user')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.role == role or (role == 'admin' and user.is_superuser):
                login(request, user)
                return redirect('dashboard') if role in ('admin', 'staff') else redirect('home')
            else:
                messages.error(request, 'Selected role does not match your account.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.role not in ('admin', 'staff'):
        return redirect('home')
    from store.models import Order, Product
    from django.contrib.auth import get_user_model
    User = get_user_model()
    context = {
        'total_orders': Order.objects.count(),
        'total_products': Product.objects.count(),
        'total_users': User.objects.filter(role='user').count(),
        'recent_orders': Order.objects.order_by('-created_at')[:10],
        'products': Product.objects.all()[:20],
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.save()
        messages.success(request, 'Profile updated!')
    return render(request, 'users/profile.html')
