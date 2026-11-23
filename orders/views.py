from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Створюємо замовлення тільки з тими полями, які реально є в моделі Order (наприклад, user)
            order = Order.objects.create(
                user=request.user
            )
            
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                
                # Зменшення залишку товару на складі
                if product.stock >= quantity:
                    product.stock -= quantity
                    product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=quantity
                )
            
            # Очищуємо кошик після оформлення
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['first_name'] = request.user.first_name
            initial_data['last_name'] = request.user.last_name
            initial_data['email'] = request.user.email
            initial_data['phone'] = getattr(request.user, 'phone', '')
            
        form = OrderCreateForm(initial=initial_data)
        
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})