from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Collection
 
 
@receiver(post_save, sender=Collection)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("Collection has beeen created")
  
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
        