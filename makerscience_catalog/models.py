# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager
from taggit.models import TaggedItem
from projects.models import Project

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
