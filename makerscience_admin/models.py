# -*- coding: utf-8 -*-
from django.db import models
from solo.models import SingletonModel

class MakerScienceStaticContent (SingletonModel):
    about = models.TextField(null=True, blank=True)
    about_team = models.TextField(null=True, blank=True)
    about_contact = models.TextField(null=True, blank=True)
    about_faq = models.TextField(null=True, blank=True)
    about_cgu = models.TextField(null=True, blank=True)


class PageViews(models.Model):
    client = models.CharField(max_length=255)
    resource_uri = models.CharField(max_length=255)
