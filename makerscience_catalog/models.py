from django.db import models
from taggit.managers import TaggableManager
from projects.models import Project

class MakerScienceProject(models.Model):
    parent = models.ForeignKey(Project)
    tags = TaggableManager()
    modified = models.DateTimeField()

    linked_resources = models.ManyToManyField("MakerScienceResource", null=True, blank=True)


class MakerScienceResource(models.Model):

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
    cost = models.PositiveIntegerField(default=0)
