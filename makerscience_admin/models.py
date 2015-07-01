# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete

from solo.models import SingletonModel

from accounts.models import ObjectProfileLink

from makerscience_forum.models import MakerSciencePost
from makerscience_profile.models import MakerScienceProfile

class MakerScienceStaticContent (SingletonModel):
    about = models.TextField(null=True, blank=True)
    about_team = models.TextField(null=True, blank=True)
    about_contact = models.TextField(null=True, blank=True)
    about_faq = models.TextField(null=True, blank=True)
    about_cgu = models.TextField(null=True, blank=True)


class PageViews(models.Model):
    client = models.CharField(max_length=255)
    resource_uri = models.CharField(max_length=255)


def clear_makerscience(sender, instance, **kwargs):
    if sender == MakerSciencePost:
        ObjectProfileLink.objects.filter(content_type__model='post',
                                      object_id=instance.parent.id).delete()
        instance.parent.delete()
    if sender == MakerScienceProfile:
        instance.parent.user.delete()

post_delete.connect(clear_makerscience, sender=MakerSciencePost)
post_delete.connect(clear_makerscience, sender=MakerScienceProfile)
