# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

from megafon.models import Post

from makerscience_catalog.models import  MakerScienceProject, MakerScienceResource

class MakerSciencePost(models.Model):

    class Meta:
        permissions = (
            ('view_makersciencepost', _("View MakerSciencePost")),
        )

    parent = models.ForeignKey(Post)

    POST_TYPE_CHOICES = (
        ("message", "Message"),
        ("question", "Moyen"),
        ("idea", "idée"),
        ("need", "Besoin"),
        ("resource", "Ressource"),
        ("event", "Événement"),
    )

    parent = models.ForeignKey(Post)
    post_type = models.CharField(max_length=8, choices=POST_TYPE_CHOICES)

    linked_projects = models.ManyToManyField(MakerScienceProject, null=True, blank=True)
    linked_resources = models.ManyToManyField(MakerScienceResource, null=True, blank=True)
