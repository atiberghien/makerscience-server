# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from haystack.query import SearchQuerySet

from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS

from dataserver.authentication import AnonymousApiKeyAuthentication
from accounts.api import ProfileResource, ObjectProfileLinkResource
from accounts.models import ObjectProfileLink
from scout.api import PlaceResource
from graffiti.api import TaggedItemResource

from makerscience_admin.api import SearchableMakerScienceResource
from makerscience_server.authorizations  import  MakerScienceAPIAuthorization
from .models import MakerScienceProfile, MakerScienceProfileTaggedItem

import json
import os
import requests

from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Hash import MD5

from base64 import urlsafe_b64encode, urlsafe_b64decode

class MakerScienceProfileResourceLight(ModelResource, SearchableMakerScienceResource):
    parent_id = fields.IntegerField('parent__id')
    first_name = fields.CharField('parent__user__first_name')
    last_name = fields.CharField('parent__user__last_name')
    address_locality = fields.CharField('location__address__address_locality', null=True)
    avatar = fields.FileField("parent__mugshot", null=True, blank=True)
    date_joined = fields.DateField("parent__user__date_joined")

    class Meta:
        queryset = MakerScienceProfile.objects.all()
        allowed_methods = ['get']
        resource_name = 'makerscience/profilelight'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        detail_uri_name = 'slug'
        excludes=["bio", "facebook", "linkedin", "twitter", "website"]
        filtering = {
            'id' : ['exact',],
            'parent_id' : ['exact',],
            'slug' : ['exact',]

        }
        limit = 6

    def dehydrate(self, bundle):
        bundle.data["lng"] = bundle.obj.location.geo.x if bundle.obj.location.geo else ""
        bundle.data["lat"] = bundle.obj.location.geo.y if bundle.obj.location.geo else ""
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
        ]


class MakerScienceProfileAuthorization(MakerScienceAPIAuthorization):
    def __init__(self):
        super(MakerScienceProfileAuthorization, self).__init__(
            create_permission_code="makerscience_profile.add_makerscienceprofile",
            view_permission_code="makerscience_profile.view_makerscienceprofile",
            update_permission_code="makerscience_profile.change_makerscienceprofile",
            delete_permission_code="makerscience_profile.delete_makerscienceprofile"
        )

class MakerScienceProfileResource(ModelResource, SearchableMakerScienceResource):
    parent = fields.OneToOneField(ProfileResource, 'parent', full=True)
    location = fields.ToOneField(PlaceResource, 'location', null=True, blank=True, full=True)

    tags = fields.ToManyField('makerscience_profile.api.MakerScienceProfileTaggedItemResource', 'tagged_items', full=True, null=True, readonly=True)

    class Meta:
        queryset = MakerScienceProfile.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        resource_name = 'makerscience/profile'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MakerScienceProfileAuthorization()
        always_return_data = True
        detail_uri_name = 'slug'
        filtering = {
            'parent' : ALL_WITH_RELATIONS,
            "location" : ['isnull', ],
            'id' : ['exact',],
            'slug' : ['exact',]
        }
        limit = 6

    def dehydrate(self, bundle):
        bundle.data["full_name"] = "%s %s" % (bundle.obj.parent.user.first_name, bundle.obj.parent.user.last_name)

        bundle.data["lng"] = bundle.obj.location.geo.x if bundle.obj.location.geo else ""
        bundle.data["lat"] = bundle.obj.location.geo.y if bundle.obj.location.geo else ""

        change_perm_code = "makerscience_profile.change_makerscienceprofile"
        bundle.data["can_edit"] = bundle.request.user.has_perm(change_perm_code, bundle.obj)

        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

    def hydrate_website(self, bundle):
        if bundle.data["website"] and (bundle.data["website"].startswith("http://") == False ^ bundle.data["website"].startswith("https://") == False):
            bundle.data["website"] = "http://" + bundle.data["website"]
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/avatar/upload%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('avatar_upload'), name="api_avatar_upload"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/activities%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_profile_activities'), name="api_profile_activities"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/contacts/activities%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_contacts_activities'), name="api_contacts_activities"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/change/password%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('change_password'), name="api_change_password"),
            url(r"^(?P<resource_name>%s)/reset/password%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('reset_password'), name="api_reset_password"),
            url(r'^(?P<resource_name>%s)/(?P<slug>[\w-]+)/send/message%s$' % (self._meta.resource_name, trailing_slash()), self.wrap_view('send_message'), name='api_send_message'),
        ]

    def send_message(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        sender_profile = MakerScienceProfile.objects.get(parent__user__id=request.user.id)
        recipient_profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        payload = dict(secret=settings.GOOGLE_RECAPTCHA_SECRET,
                       response=data['recaptcha_response'])

        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        resp = json.loads(r.text)
        if resp["success"]:
            try:
                subject = "Message de %s sur Makerscience" % sender_profile.parent.get_full_name_or_username()
                from_email = 'Makerscience <no-reply@makerscience.fr>'
                to = recipient_profile.parent.user.email
                text_content = render_to_string('notifications/message.txt', {'sender' : sender_profile, 'body' : data["body"], 'recipient' : recipient_profile})
                html_content = render_to_string('notifications/message.html', {'sender' : sender_profile, 'body' : data["body"], 'recipient' : recipient_profile})
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                return self.create_response(request, {'success': False, 'reason' : 'EMAIL_SENDING_FAIL'})
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False, 'reason' : 'RECAPTCHA_ERROR'})

    def reset_password(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        aes = AES.new(settings.AES_KEY, AES.MODE_CFB, settings.AES_IV)

        email = request.GET.get('email', None)
        hash = request.GET.get('hash', None)
        password = request.GET.get('password', None)

        try :
            profile = MakerScienceProfile.objects.get(parent__user__email=email)

            if hash and password :
                decoded_email = urlsafe_b64decode(str(hash))
                decrypted_email = aes.decrypt(decoded_email)

                if decrypted_email == email:
                    profile.parent.user.set_password(password)
                    profile.parent.user.save()
                    return self.create_response(request, {'success': True, 'error' : 'EMAIL_RESETED'})
                else:
                    return self.create_response(request, {'success': False, 'error' : 'EMAIL_MISSMATCH'})
            else:
                password_reset_url = u"%s/%s/?email=%s" % (settings.RESET_PASSWORD_URL, urlsafe_b64encode(aes.encrypt(email)), email.encode('utf-8'))
                try:
                    subject = "Ré-initialisation de votre mot de passe sur Makerscience"
                    from_email = 'Makerscience <no-reply@makerscience.fr>'
                    to = profile.parent.user.email
                    text_content = render_to_string('notifications/reset_password.txt', {'password_reset_url' : password_reset_url, 'recipient' : profile })
                    html_content = render_to_string('notifications/reset_password.html', {'password_reset_url' : password_reset_url, 'recipient' : profile })
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except:
                    return self.create_response(request, {'success': False, 'reason' : 'EMAIL_SENDING_FAIL'})
                return self.create_response(request, {'success': True, 'error' : 'EMAIL_SENT'})

        except MakerScienceProfile.DoesNotExist :
            return self.create_response(request, {'success': False, 'error' : 'UNKNOWN_PROFILE'})


    def change_password(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        if profile.parent.user.id != request.user.id:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        profile.parent.user.set_password(data['password'])
        profile.parent.user.save()

        return self.create_response(request, {'success': True, 'msg' : 'password reseted'})

    def avatar_upload(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        file = request.FILES['file']

        old_file_path = None
        if profile.parent.mugshot :
            old_file_path = profile.parent.mugshot.path

        profile.parent.mugshot = file
        profile.parent.save()

        if old_file_path and os.path.isfile(old_file_path):
            os.remove(old_file_path)

        return self.create_response(request, {
            'avatar': profile.parent.mugshot.url,
        })

    def get_profile_activities(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        limit = request.GET.get('limit', None)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        activities = []
        all_activities = ObjectProfileLink.objects.filter(profile=profile.parent, isValidated=True).order_by('-created_on')
        for activity in all_activities:
            activities.append({
                'description' : render_to_string('notifications/activity.html', {'activity': activity, 'egocentric':True}),
                'created_on' : activity.created_on
            })
            if limit and len(activities) == int(limit):
                break

        return self.create_response(request, {
            'metadata' : {
                'limit' : int(limit),
                'total_count' : all_activities.count()
            },
            'objects': activities,
        })

    def get_contacts_activities(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        limit = request.GET.get('limit', None)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        contact_ids = profile.parent.objectprofilelink_set.filter(level=40).values_list('object_id', flat=True) #Must return IDs of MakerScienceProfile
        contact_ids = MakerScienceProfile.objects.filter(id__in=[int(i) for i in contact_ids]).values_list('parent__id', flat=True)

        activities = []
        all_activities = ObjectProfileLink.objects.filter(profile__in=contact_ids, isValidated=True).order_by('-created_on')
        for activity in all_activities:
            activities.append({
                'description' : render_to_string('notifications/activity.html', {'activity': activity, 'egocentric':False}),
                'created_on' : activity.created_on
            })
            if limit and len(activities) == int(limit):
                break

        return self.create_response(request, {
            'metadata' : {
                'limit' : int(limit),
                'total_count' : all_activities.count()
            },
            'objects': activities,
        })

class MakerScienceProfileTaggedItemResource(TaggedItemResource):

    class Meta:
        queryset = MakerScienceProfileTaggedItem.objects.all()
        resource_name = 'makerscience/profiletaggeditem'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        default_format = "application/json"
        filtering = {
            "tag" : ALL_WITH_RELATIONS,
            "object_id" : ['exact', ],
            'tag_type' : ['exact', ]
        }
        always_return_data = True
        limit = 0

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_id>\d+?)/(?P<tag_type>\w+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_id>\d+?)/similars%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('get_similars'),
               name="api_get_similars"),
        ]
