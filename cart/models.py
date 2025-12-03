from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"
    


    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def total_price(self):
        return sum(item.price_per_item * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        unique_together = ("cart", "product")
        ordering = ["-id"]

        
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.price_per_item * self.quantity
    

