from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



# Create your models here.

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Seller', 'Seller'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')
    
    contact_number = models.CharField(max_length=15, blank=True, null=True, help_text="Optional contact number")
    
    security_pass = models.CharField(max_length=100, blank=True, null=True, help_text="Required only if you sign up as Seller")
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, help_text="Optional profile picture")

    birth_date = models.DateField(blank=True, null=True, help_text="Optional birth date")
    
    address = models.TextField(blank=True, null=True, help_text="Optional address")
    
    
    def __str__(self):
        return self.username
    
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer_profile")
    address = models.TextField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    
    def __str__(self):
        return f"Customer Profile - {self.user.username}"
    
class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="seller_profile")
    email_address = models.EmailField(blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_address = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Seller Profile - {self.user.username}"
    
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:
        from .models import SellerProfile
        SellerProfile.objects.create(user=instance)
    
    




