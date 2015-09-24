# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db import models
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from scout.models import PostalAddress, Place
from taggit.models import TaggedItem
from taggit.managers import TaggableManager
from guardian.shortcuts import assign_perm
from autoslug import AutoSlugField
from django.conf import settings
from guardian.shortcuts import assign_perm

class MakerScienceProfileTaggedItem (TaggedItem):
    PROFILE_TAG_TYPE_CHOICES = (
        ('SK', 'Compétences'),
        ('IN', 'Intêrets'),
    )
    tag_type = models.CharField(max_length=2, choices=PROFILE_TAG_TYPE_CHOICES)

class MakerScienceProfile(models.Model):
    slug = AutoSlugField(always_update=True,
                         unique=True,
                         populate_from=lambda instance: instance.parent.get_full_name_or_username())
    parent = models.ForeignKey(Profile)
    activity = models.CharField(max_length=255)
    bio = models.TextField()
    location = models.ForeignKey(Place, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    tags = TaggableManager(through=MakerScienceProfileTaggedItem, blank=True)

    facebook = models.CharField(max_length=500, null=True, blank=True)
    twitter = models.CharField(max_length=500, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)
    contact_email = models.CharField(max_length=500, null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return "Profil Makerscience de %s" % self.parent.get_full_name_or_username()


@receiver(post_save, sender=Profile)
def create_profile_on_user_signup(sender, created, instance, **kwargs):
    if created:
        location = Place.objects.create(address=PostalAddress.objects.create())
        MakerScienceProfile.objects.create(parent=instance, location=location)

@receiver(post_save, sender=MakerScienceProfile)
def assign_profile_permissions(sender, created, instance, **kwargs):
    change_perm_code = 'makerscience_profile.change_makerscienceprofile'
    assign_perm('makerscience_profile.change_makerscienceprofile', user_or_group=instance.parent.user, obj=instance)
    assign_perm('auth.change_user', user_or_group=instance.parent.user, obj=instance.parent.user)


@receiver(post_save, sender=User)
def allow_user_to_create_MS_resources_and_project(sender, instance, created, *args, **kwargs):
    """
    Here we assign all newly created users to the group 'ma_authenticated_users'
    If this group does not exists we create it and give permissions from settings
    variable MS_AUTHENTICATED_USERS_PERMISSIONS
    """
    # Check if authenticated_user group exists, if not create it and add following perms
    group, created = Group.objects.get_or_create(name='ms_authenticated_users')

    # assign perms to group
    permissions = getattr(settings, 'MS_AUTHENTICATED_USERS_PERMISSIONS')
    for permission in permissions:
        try:
            assign_perm(permission, group)
        except:
            print permission
    # assign user to group
    instance.groups.add(group)
