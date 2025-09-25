from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": 1}, price_per_item=product.price)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total = 0
    for item in items:
        item.subtotal =  item.product.price * item.quantity
        total += item.subtotal

    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    
    return render(request, 'cart/cart_detail.html', context)




@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect("cart_detail")



@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.warning(request, "Cart cleared.")
    return redirect("cart_detail")


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.warning(request, f"{cart_item.product.name} removed from cart.")
    return redirect("cart_detail")





