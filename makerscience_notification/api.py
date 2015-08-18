# -*- coding: utf-8 -*-
from django.template.loader import render_to_string

from tastypie.resources import ModelResource
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.authorization import DjangoAuthorization

from notifications.models import Notification
from notifications.views import live_unread_notification_count, live_unread_notification_list

from accounts.api import UserResource
from dataserver.authentication import AnonymousApiKeyAuthentication

class NotificationResource(ModelResource):
    actor_content_type = fields.CharField(attribute='actor_content_type__model', null=True)
    target_content_type = fields.CharField(attribute='target_content_type__model', null=True)
    action_object_content_type = fields.CharField(attribute='action_object_content_type__model', null=True)

    recipient_id = fields.CharField(attribute='recipient__id', null=True)

    class Meta:
        queryset = Notification.objects.all()
        allowed_methods = ['get', 'patch']
        resource_name = 'notification'
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        limit = 0
        excludes = ['data', 'emailed', 'public']
        filtering = {
            'recipient_id' : ['exact']
        }

    def dehydrate_description(self, bundle):
        return render_to_string('notifications/notification.html', {'notif': bundle.obj})
