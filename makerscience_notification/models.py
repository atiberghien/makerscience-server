# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from notifications import notify
from notifications.models import Notification

from accounts.models import ObjectProfileLink

from makerscience_profile.models import MakerScienceProfile
from makerscience_catalog.models import MakerScienceProject, MakerScienceResource
from makerscience_forum.models import MakerSciencePost

from datetime import datetime, timedelta

def create_notification(sender, instance, created, **kwargs):
    activity = instance
    if sender == ObjectProfileLink and created:
        actor = MakerScienceProfile.objects.get(parent=activity.profile)

        is_not_actor = lambda x: x is not actor.parent.id

        if activity.level == 50:
            tag = activity.content_object.tag
            profile_ids = ObjectProfileLink.objects.filter(level=51,
                                                   content_type=ContentType.objects.get_for_model(tag),
                                                   object_id=tag.id).values_list('profile', flat=True)

            for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                notify.send(actor,
                            recipient=profile.parent.user,
                            verb=u'tagged',
                            action_object=tag,
                            target=activity.content_object.content_object)
        elif activity.level == 0:
            if activity.isValidated == False: #someome ask to join project team
                profile_ids = ObjectProfileLink.objects.filter(level=0,
                                                               isValidated=True,
                                                               content_type=ContentType.objects.get_for_model(activity.content_object),
                                                               object_id=activity.content_object.id).values_list('profile', flat=True)

                for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                    notify.send(actor,
                                recipient=profile.parent.user,
                                target=activity.content_object,
                                verb=u'team_requested')
            else :#someone has created a project
                profile_ids = ObjectProfileLink.objects.filter(level=40,
                                                               content_type=ContentType.objects.get_for_model(actor),
                                                               object_id=actor.id).values_list('profile', flat=True)

                for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                    notify.send(actor,
                                recipient=profile.parent.user,
                                action_object=activity.content_object,
                                verb=u'created')
        elif activity.level == 1:
                profile_ids = ObjectProfileLink.objects.filter(level=0,
                                                               isValidated=True,
                                                               content_type=ContentType.objects.get_for_model(activity.content_object),
                                                               object_id=activity.content_object.id).values_list('profile', flat=True)

                for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                    notify.send(actor,
                                recipient=profile.parent.user,
                                target=activity.content_object,
                                verb=u'help_proposed')
        elif activity.level == 10:
            if activity.isValidated == False: #someome ask to join project team
                profile_ids = ObjectProfileLink.objects.filter(level=10,
                                                               isValidated=True,
                                                               content_type=ContentType.objects.get_for_model(activity.content_object),
                                                               object_id=activity.content_object.id).values_list('profile', flat=True)

                for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                    notify.send(actor,
                                recipient=profile.parent.user,
                                target=activity.content_object,
                                verb=u'coauthor_requested')
            else :#someone has created a project
                profile_ids = ObjectProfileLink.objects.filter(level=40,
                                                               content_type=ContentType.objects.get_for_model(actor),
                                                               object_id=actor.id).values_list('profile', flat=True)

                for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                    notify.send(actor,
                                recipient=profile.parent.user,
                                action_object=activity.content_object,
                                verb=u'created')
        elif activity.level == 11:
                profile_ids = ObjectProfileLink.objects.filter(level=10,
                                                               isValidated=True,
                                                               content_type=ContentType.objects.get_for_model(activity.content_object),
                                                               object_id=activity.content_object.id).values_list('profile', flat=True)

                for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                    notify.send(actor,
                                recipient=profile.parent.user,
                                target=activity.content_object,
                                verb=u'similars_shared')
        elif activity.level == 5: #someone has been invited to join  a project team
            notify.send(MakerScienceProfile.objects.get(slug=activity.detail),
                        recipient=actor.parent.user,
                        target=activity.content_object,
                        verb=u'team_invited')
        elif activity.level == 6: #someone has been invited to help  a project team
            notify.send(MakerScienceProfile.objects.get(slug=activity.detail),
                        recipient=actor.parent.user,
                        target=activity.content_object,
                        verb=u'help_invited')
        elif activity.level == 7: #someone added a news to a project
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 2]).distinct('profile').values_list('profile', flat=True)

            for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                notify.send(actor,
                            recipient=actor.parent.user,
                            target=activity.content_object,
                            verb=u'annonced')
        elif activity.level == 15: #someone has been invited to join  co-author
            notify.send(MakerScienceProfile.objects.get(slug=activity.profile),
                        recipient=actor.parent.user,
                        target=activity.content_object,
                        verb=u'coauthor_invited')
        elif activity.level == 16: #someone has been invited to shared his similar resource
            notify.send(MakerScienceProfile.objects.get(slug=activity.detail),
                        recipient=actor.parent.user,
                        target=activity.content_object,
                        verb=u'similar_resource_invited')
        elif activity.level in [2, 12, 33]: #liked content where the recipient is involved (creator, member)
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 10, 11, 30, 31]).distinct('profile').values_list('profile', flat=True)

            for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                notify.send(actor,
                            recipient=profile.parent.user,
                            action_object=activity.content_object,
                            verb=u'liked')
        elif activity.level in [3, 13]: #commented content where the recipient is involved (creator, member)
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 10, 11]).distinct('profile').values_list('profile', flat=True)

            for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
                notify.send(actor,
                            recipient=profile.parent.user,
                            action_object=activity.content_object,
                            verb=u'commented')
        elif activity.level in [4, 14]: #scored content where the recipient is involved (creator, member)
            profile_ids = ObjectProfileLink.objects.filter(level__in=[0, 1, 10, 11]).distinct('profile').values_list('profile', flat=True)

            for profile in MakerScienceProfile.objects.filter(parent__id__in=filter(is_not_actor, profile_ids)):
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

def generate_notif_description(sender, instance, created, **kwargs):
    if created or instance.data == None:
        instance.data = {'description' : render_to_string('notifications/notification.html', {'notif': instance})}
        instance.save()

post_save.connect(generate_notif_description, sender=Notification)


def send_notifications_by_mail(frequency):
    for profile in MakerScienceProfile.objects.all():
        notifs = profile.parent.user.notifications.all()
        if profile.notif_subcription_freq == frequency:
            if frequency == 'DAILY':
                time_threshold = datetime.now() - timedelta(hours=24)
            elif frequency == 'WEEKLY':
                time_threshold = datetime.now() - timedelta(weeks=1)
            notifs = notifs.filter(timestamp__gte=time_threshold)

            subject = "Notifications Makerscience"
            from_email = 'no-reply@makerscience.fr'
            to = profile.parent.user.email
            context = {
                'frequency' : frequency,
                'notifs' : notifs,
                'base_url' : settings.MAKERSCIENCE_BASE_URL
            }

            text_content = render_to_string('notifications/notif_multiple.txt', context)
            html_content = render_to_string('notifications/notif_multiple.html', context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
