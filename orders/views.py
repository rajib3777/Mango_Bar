from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart,CartItem
from django.contrib.auth.decorators import login_required

@login_required






def checkout(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart_detail", cart_id=cart.id)
    
    total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
    )

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price_per_item=cart_item.product.price,
        )
    
    cart.items.all().delete()
    messages.success(request, f"Order #{order.id} placed successfully!")
    
    return render(request, "orders/checkout.html", {"cart": cart})




def order_list(request):
    orders = Order.objects.all()
    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_detail.html", {"order": order})



