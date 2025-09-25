from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,CustomerProfile,SellerProfile


@receiver(post_save, sender=CustomUser)

def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_active:
        if instance.role == "Customer":
            CustomerProfile.objects.get_or_create(user=instance)
        elif instance.role == "Seller":
            SellerProfile.objects.get_or_create(user=instance)

            




