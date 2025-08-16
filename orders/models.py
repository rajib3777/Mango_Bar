from django.db import models



# Create your models here.

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name} for {self.product_name}"
    def total_price(self, price_per_item):
        return self.quantity * price_per_item
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in Order {self.order.id}"
    
    def total_price(self):
        return self.quantity * self.price_per_item
    
    class Meta:
        ordering = ['order', 'product_name']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        
class Cart(models.Model):
    customer_name = models.CharField(max_length=100)
    items = models.ManyToManyField(OrderItem, related_name='carts', blank=True)

    def __str__(self):
        return f"Cart for {self.customer_name}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in Cart for {self.cart.customer_name}"
    
    def total_price(self):
        return self.quantity * self.price_per_item
    
    class Meta:
        ordering = ['cart', 'product_name']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        
