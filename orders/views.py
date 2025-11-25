from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings



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
        
        
        product = cart_item.product
        
        if hasattr(product, "quantity"):
            product.quantity = max(product.quantity - cart_item.quantity, 0)
        elif hasattr(product, "stock"):
            product.stock = max(product.stock - cart_item.quantity, 0)
        product.save()
    
    cart.items.all().delete()
    
    try:
        send_mail(
            subject=f"Order #{order.id} Confirmation",
            message=(
                f"Hello {request.user.email},\n\n"
                f"Your order has been placed successfully!\n\n"
                f"Order ID: {order.id}\n"
                f"Total Amount: {order.total_amount} BDT\n"
                f"Status: Pending\n\n"
                "Thank you for ordering from Mango Bar! 🥭"
            ), 
            
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[request.user.email] if request.user.email else [],
            fail_silently=False,
        )
    except Exception as e:
        print("Checkout Email Failed:", e)

    
    
    messages.success(request, f"Order #{order.id} placed successfully!")
    
    return render(request, "orders/checkout.html", {"cart": cart})




def order_list(request):
    orders = Order.objects.all()
    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_detail.html", {"order": order})



