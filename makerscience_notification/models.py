# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType

from notifications import notify

from accounts.models import ObjectProfileLink

from makerscience_profile.models import MakerScienceProfile

def create_notification(sender, instance, created, **kwargs):
    activity = instance
    if created:
        actor = MakerScienceProfile.objects.get(parent=activity.profile)
        if activity.level == 50:
            tag = activity.content_object.tag
            profile_ids = ObjectProfileLink.objects.filter(level=51,
                                                   content_type=ContentType.objects.get_for_model(tag),
                                                   object_id=tag.id).values_list('profile', flat=True)

            for profile in MakerScienceProfile.objects.filter(parent__id__in=profile_ids):
                notify.send(actor,
                            recipient=profile.parent.user,
                            verb=u'tagged',
                            action_object=tag,
                            target=activity.content_object.content_object)
        elif activity.level in [0, 10, 30]:
            profile_ids = ObjectProfileLink.objects.filter(level=40,
                                                        content_type=ContentType.objects.get_for_model(actor),
                                                           object_id=actor.id).values_list('profile', flat=True)
            for profile in MakerScienceProfile.objects.filter(parent__id__in=profile_ids):
                notify.send(actor,
                            recipient=profile.parent.user,
                            action_object=activity.content_object,
                            verb=u'created')
        elif activity.level in [2, 12, 33]: #liked content where the recipient is involved (creator, member)
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 10, 11, 30, 31]).distinct('profile').values_list('profile', flat=True)
            for profile in MakerScienceProfile.objects.filter(parent__id__in=profile_ids):
                notify.send(actor,
                            recipient=profile.parent.user,
                            action_object=activity.content_object,
                            verb=u'liked')
        elif activity.level in [3, 13]: #commented content where the recipient is involved (creator, member)
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 10, 11]).distinct('profile').values_list('profile', flat=True)
            for profile in MakerScienceProfile.objects.filter(parent__id__in=profile_ids):
                notify.send(actor,
                            recipient=profile.parent.user,
                            action_object=activity.content_object,
                            verb=u'commented')
        elif activity.level in [4, 14]: #scored content where the recipient is involved (creator, member)
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 10, 11]).distinct('profile').values_list('profile', flat=True)
            for profile in MakerScienceProfile.objects.filter(parent__id__in=profile_ids):
                notify.send(actor,
                            recipient=profile.parent.user,
                            action_object=activity.content_object,
                            verb=u'scored')
        elif activity.level == 40: #added the recipient as friend
            notify.send(actor,
                        recipient=activity.content_object.parent.user,
                        verb=u'friendship')
        elif activity.level == 41: #mentionned the recipient in a discussion
            mentionned_profile = MakerScienceProfile.objects.get(slug=activity.detail)
            notify.send(actor,
                        recipient=mentionned_profile.parent.user,
                        verb=u'mentionned',
                        target=activity.content_object)

post_save.connect(create_notification, sender=ObjectProfileLink)
