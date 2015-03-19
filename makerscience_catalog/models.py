from django.db import models
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager
from projects.models import Project


class MakerScienceProject(models.Model):
    class Meta:
        permissions = (
            ('view_makerscienceproject', _("View MakerScienceProject")),
        )

    parent = models.ForeignKey(Project)
    tags = TaggableManager()
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
    tags = TaggableManager()
    modified = models.DateTimeField()

    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=30)
    cost = models.CharField(max_length=30)

    linked_resources = models.ManyToManyField("MakerScienceResource", null=True, blank=True)

    featured = models.BooleanField(default=False)
