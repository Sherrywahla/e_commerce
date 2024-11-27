from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Category,Product
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(
            username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'stores/register.html')


def home(request):
    products = Product.objects.all()
    return render(request, 'stores/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    reviews = product.reviews.all()
    total_reviews = reviews.count()
    average_rating = 0
    if total_reviews > 0:
        average_rating = sum([review.rating for review in reviews]) / total_reviews

    features = [feature.strip()
                for feature in product.features.split('\n') if feature.strip()]

    total_qty_in_cart = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(
                cart=cart, product=product).first()
            if cart_item:
                total_qty_in_cart = cart_item.quantity
        except Cart.DoesNotExist:
            pass  
    else:
        cart = request.session.get('cart', {})
        if str(product.id) in cart:
            total_qty_in_cart = cart[str(product.id)]['quantity']

    return render(request, 'stores/product_detail.html', {
        'product': product,
        'features': features,
        'total_qty_in_cart': total_qty_in_cart,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'reviews': reviews,
        'range_5': range(1, 6)
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'stores/category_products.html', {'category': category, 'products': products})

