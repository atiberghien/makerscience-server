# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver

from guardian.shortcuts import assign_perm, remove_perm
from taggit.managers import TaggableManager
from taggit.models import TaggedItem

from scout.models  import Place, PostalAddress
from projects.models import Project
from accounts.models import ObjectProfileLink


class MakerScienceProjectTaggedItem (TaggedItem):
    PROJECT_TAG_TYPE_CHOICES = (
        ('th', 'Thématique'),
        ('tg', 'Cibles visées'),
        ('fm', 'Formats'),
        ('nd', 'Besoins'),
    )
    tag_type = models.CharField(max_length=2, choices=PROJECT_TAG_TYPE_CHOICES)


class MakerScienceResourceTaggedItem (TaggedItem):
    RESOURCE_TAG_TYPE_CHOICES = (
        ('th', 'Thématique'),
        ('tg', 'Cibles visées'),
        ('fm', 'Formats'),
        ('rs', 'Ressources nécessaires'),
    )
    tag_type = models.CharField(max_length=2, choices=RESOURCE_TAG_TYPE_CHOICES)

class MakerScienceProject(models.Model):
    parent = models.ForeignKey(Project)
    tags = TaggableManager(through=MakerScienceProjectTaggedItem, blank=True)
    modified = models.DateTimeField()

    linked_resources = models.ManyToManyField("MakerScienceResource", null=True, blank=True)

    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.parent.title

    class Meta :
        ordering = ['parent__created_on',]

@receiver(post_save, sender=MakerScienceProject)
def assign_place_to_project(sender, created, instance, **kwargs):
    if instance.parent.location is None:
        instance.parent.location = Place.objects.create(address=PostalAddress.objects.create())
        instance.parent.save()


class MakerScienceResource(models.Model):
    parent = models.ForeignKey(Project)
    tags = TaggableManager(through=MakerScienceResourceTaggedItem, blank=True)
    modified = models.DateTimeField()

    duration = models.CharField(max_length=30)

    linked_resources = models.ManyToManyField("MakerScienceResource", null=True, blank=True)

    featured = models.BooleanField(default=False)

    class Meta :
        ordering = ['parent__created_on',]


@receiver(post_save, sender=ObjectProfileLink)
def assign_permissions(sender, created, instance, **kwargs):
    if instance.level in [0, 10] and instance.isValidated:
        change_perm_code = "makerscience_catalog.change_%s" % instance.content_object._meta.model_name
        assign_perm(change_perm_code, user_or_group=instance.profile.user, obj=instance.content_object)

@receiver(post_delete, sender=ObjectProfileLink)
def remove_permissions(sender, instance, **kwargs):
    if instance.level in [0, 10]:
        try:
            change_perm_code = "makerscience_catalog.change_%s" % instance.content_object._meta.model_name
            remove_perm(change_perm_code, user_or_group=instance.profile.user, obj=instance.content_object)
        except:
            pass
