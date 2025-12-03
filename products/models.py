from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField



User = settings.AUTH_USER_MODEL
                              

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('image', folder='categories/', null=True, blank=True)


    def __str__(self):
        return self.name


class Product(models.Model):
    Seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products",db_column="seller_id", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # quantity = models.PositiveIntegerField(default=0)
    image = CloudinaryField('image', folder='products/', null=True, blank=True) 

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image', folder='product_images/')
    def __str__(self):
        return f"Image of {self.product.name}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # 1-5 scale
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        unique_together = ('product', 'user')
        
    def __str__(self):
        return f"Review by {self.user} on {self.product}"
    


    


    