# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db import models
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from scout.models import PostalAddress
from taggit.models import TaggedItem
from taggit.managers import TaggableManager
from guardian.shortcuts import assign_perm
from autoslug import AutoSlugField

class MakerScienceProfileTaggedItem (TaggedItem):
    PROFILE_TAG_TYPE_CHOICES = (
        ('SK', 'Compétences'),
        ('IN', 'Intêrets'),
    )
    tag_type = models.CharField(max_length=2, choices=PROFILE_TAG_TYPE_CHOICES)

class MakerScienceProfile(models.Model):
    slug = AutoSlugField(always_update=True,
                         populate_from=lambda instance: instance.parent.get_full_name_or_username())
    parent = models.ForeignKey(Profile)
    activity = models.CharField(max_length=255)
    bio = models.TextField()
    location = models.ForeignKey(PostalAddress, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager(through=MakerScienceProfileTaggedItem, blank=True)

    facebook = models.CharField(max_length=500, null=True, blank=True)
    twitter = models.CharField(max_length=500, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)
    contact_email = models.CharField(max_length=500, null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)


@receiver(post_save, sender=Profile)
def create_profile_on_user_signup(sender, created, instance, **kwargs):
    if created:
        location = PostalAddress.objects.create()
        MakerScienceProfile.objects.create(parent=instance, location=location)

@receiver(post_save, sender=User)
def allow_user_to_create_MS_resources_and_project(sender, instance, created, *args, **kwargs):
    """
    We also need to assign all non MS-specific permissions for objects that come with MSResources/MSProjects:
    - Project
    - ProjectSheet
    - Pro

    """
    # Check if authenticated_user group exists, if not create it and add following perms
    group, created = Group.objects.get_or_create(name='ms_authenticated_users')
    if created:
        # assign perms to group
        assign_perm('makerscience_catalog.add_makerscienceproject', group)
        assign_perm('makerscience_catalog.view_makerscienceproject', group)
        assign_perm('makerscience_catalog.add_makerscienceresource', group)
        assign_perm('makerscience_catalog.view_makerscienceresource', group)

        assign_perm('makerscience_profile.change_makerscienceprofile', group)
        assign_perm('makerscience_profile.add_makerscienceprofiletaggeditem', group)
        assign_perm('makerscience_profile.change_makerscienceprofiletaggeditem', group)
        assign_perm('makerscience_profile.delete_makerscienceprofiletaggeditem', group)

        assign_perm('makerscience_forum.change_makersciencepost', group)
        assign_perm('makerscience_forum.add_makersciencepost', group)
        assign_perm('makerscience_forum.change_makersciencepost', group)
        assign_perm('makerscience_forum.delete_makersciencepost', group)

    # assign user to group
    instance.groups.add(group)
