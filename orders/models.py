from django.db import models
from products.models import Product
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.conf import settings


User = settings.AUTH_USER_MODEL



# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    
    def total_price(self):
        return self.quantity * self.price_per_item
    
    class Meta:
        ordering = ['order', 'product']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        

