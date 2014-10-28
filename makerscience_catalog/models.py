from django.db import models
from taggit.managers import TaggableManager
from projects.models import Project

class MakerScienceProject(models.Model):
    parent = models.ForeignKey(Project)
    
    tags = TaggableManager()