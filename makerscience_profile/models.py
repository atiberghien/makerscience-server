from django.db import models
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from scout.models import PostalAddress

# Create your models here.


class MakerScienceProfile(models.Model):
    parent = models.ForeignKey(Profile)
    activity = models.CharField(max_length=255)
    bio = models.TextField()
    location = models.ForeignKey(PostalAddress, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    
    
@receiver(post_save, sender=Profile)
def create_profile_on_user_signup(sender, created, instance, **kwargs):
    if created:
        MakerScienceProfile.objects.create(parent=instance)