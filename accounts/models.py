from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'seller'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
    )
    
    contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Optional contact number"
    )
    
    security_pass = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Required only if you sign up as Seller"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="Optional profile picture"
    )

    def __str__(self):
        return self.username


