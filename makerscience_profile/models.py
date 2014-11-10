from django.db import models
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

# Create your models here.


class MakerScienceProfile(models.Model):
    parent = models.ForeignKey(Profile)
    
    
@receiver(post_save, sender=Profile)
def create_profile_on_user_signup(sender, created, instance, **kwargs):
    if created:
        MakerScienceProfile.objects.create(parent=instance)