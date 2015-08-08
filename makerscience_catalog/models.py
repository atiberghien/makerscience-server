# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager
from taggit.models import TaggedItem

from scout.models  import Place, PostalAddress
from projects.models import Project

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

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
    class Meta:
        permissions = (
            ('view_makerscienceproject', _("View MakerScienceProject")),
        )

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

    class Meta:
        permissions = (
            ('view_makerscienceresource', _("View MakerScienceResource")),
        )

    LEVEL_CHOICES = (
        ("1", "Facile"),
        ("2", "Moyen"),
        ("3", "Difficile")
    )

    parent = models.ForeignKey(Project)
    tags = TaggableManager(through=MakerScienceResourceTaggedItem, blank=True)
    modified = models.DateTimeField()

    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=30)
    cost = models.CharField(max_length=30)

    linked_resources = models.ManyToManyField("MakerScienceResource", null=True, blank=True)

    featured = models.BooleanField(default=False)

    class Meta :
        ordering = ['parent__created_on',]
