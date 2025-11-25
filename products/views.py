from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product
from django.db.models import Q
from .forms import ProductForm
from cart.models import Cart
from accounts.decorators import role_required
from .forms import StockUpdateForm




# Product List
def product_list(request):
    query = request.GET.get("q")
    category_id = request.GET.get("category")
    
    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)
        
    categories = Category.objects.all()
    return render(request,"products/product_list.html",{
        "products": products,
        "categories": categories
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    return render(request, "products/product_detail.html", {"product": product,"cart": cart})


@login_required
@role_required('Seller')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user 
            product.save()
            messages.success(request, "Product Created Successfully!")
            return redirect("product_list")
        else:
            messages.error(request, "Please correct the errors below")
            
    else:
        form = ProductForm()
        
    return render(request, "products/product_create.html", {"form": form})



@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart_detail")



@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user.role != "seller" or request.user != product.seller:
        messages.error(request,"You are not allowed to update this product.")
        return redirect("product_list")
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Update Successfully!")
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
        
        categories = Category.objects.all()
        return render(request, "products/product_update.html",{
            "form": form,
            "product": product,
            "categories": categories
        })
        
        
        
        
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user != product.seller and not request.user.is_superuser:
        messages.error(request,"You are not allowed to delete this product.")
        return redirect("product_list")
    
    if request.method == "POST":
        product.delete()
        messages.success(request,"Product deleted successfully.")
        return redirect("product_list")
    
    return render(request, "products/product_delete.html", {"product": product})



@login_required
@role_required('Admin','Seller')
def update_product_quantity(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.role == "Seller" and product.seller != request.user:
        messages.error(request,"You can only update your own product stock.")
        return redirect('seller_dashboard')
    
    if request.method == "POST":
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            delta = form.cleaned_data['delta']
            product.stock = (product.stock or 0) + delta
            product.save()
            messages.success(request, f"Stock updated by +{delta} for {product.name}.")
        else:
            messages.error(request, "Invalid quantity.")
            
    return redirect('admin-dashboard' if request.user.role == "Admin" or request.user.is_superuser else 'seller-dashboard')
