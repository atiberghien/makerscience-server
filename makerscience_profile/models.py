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
        location, created = PostalAddress.objects.create()
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

        assign_perm('accounts.add_objectprofilelink', group)
        assign_perm('accounts.change_objectprofilelink', group)
        assign_perm('accounts.delete_objectprofilelink', group)
        assign_perm('accounts.change_profile', group)
        assign_perm('accounts.view_profile', group)
        assign_perm('bucket.add_bucket', group)
        assign_perm('bucket.change_bucket', group)
        assign_perm('bucket.view_bucket', group)
        assign_perm('bucket.add_bucketfile', group)
        assign_perm('scout.change_postaladdress', group)
        assign_perm('scout.view_postaladdress', group)
        assign_perm('django_comments.add_comment', group)
        assign_perm('django_comments.change_comment', group)
        assign_perm('django_comments.delete_comment', group)
        assign_perm('django_comments.add_commentflag', group)
        assign_perm('django_comments.change_commentflag', group)
        assign_perm('projects.add_project', group)
        assign_perm('projects.change_project', group)
        assign_perm('projects.add_projectprogress', group)
        assign_perm('projects.change_projectprogress', group)
        assign_perm('projects.delete_projectprogress', group)
        assign_perm('projects.add_projectprogressrange', group)
        assign_perm('projects.change_projectprogressrange', group)
        assign_perm('projects.delete_projectprogressrange', group)
        assign_perm('projectsheet.add_projectsheet', group)
        assign_perm('projectsheet.change_projectsheet', group)
        assign_perm('projectsheet.add_projectsheetquestion', group)
        assign_perm('projectsheet.change_projectsheetquestion', group)
        assign_perm('projectsheet.add_projectsheetquestionanswer', group)
        assign_perm('projectsheet.change_projectsheetquestionanswer', group)
        assign_perm('taggit.add_tag', group)
        assign_perm('taggit.change_tag', group)
        assign_perm('taggit.delete_tag', group)
        assign_perm('taggit.add_taggeditem', group)
        assign_perm('taggit.change_taggeditem', group)
        assign_perm('taggit.delete_taggeditem', group)

    # assign user to group
    instance.groups.add(group)
