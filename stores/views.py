from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, CartItem, Category, Order, OrderItem, Product
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

        if self.request.user.is_authenticated:
            session_cart = self.request.session.get('cart', {})
            if session_cart:
                cart, created = Cart.objects.get_or_create(
                    user=self.request.user)

                for product_id, item in session_cart.items():
                    product = get_object_or_404(Product, id=product_id)
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart, product=product)

                    if not created:
                        cart_item.quantity += item['quantity']
                    else:
                        cart_item.quantity = item['quantity']
                    cart_item.save()

                del self.request.session['cart']

                messages.success(
                    self.request, 'Cart items migrated to your account')

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

