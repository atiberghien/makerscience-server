from datetime import datetime
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

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
from .models import MakerScienceProfile, MakerScienceProfileTaggedItem

import json
import os


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

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
        ]


class MakerScienceProfileResource(ModelResource, SearchableMakerScienceResource):
    parent = fields.OneToOneField(ProfileResource, 'parent', full=True)
    location = fields.ToOneField(PlaceResource, 'location', null=True, blank=True, full=True)

    tags = fields.ToManyField('makerscience_profile.api.MakerScienceProfileTaggedItemResource', 'tagged_items', full=True, null=True, readonly=True)

    class Meta:
        queryset = MakerScienceProfile.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        resource_name = 'makerscience/profile'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
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

        change_perm_code = "makerscience_profile.change_makerscienceprofile"
        bundle.data["can_edit"] = bundle.request.user.has_perm(change_perm_code, bundle.obj)

        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/avatar/upload%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('avatar_upload'), name="api_avatar_upload"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/activities%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_profile_activities'), name="api_profile_activities"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w-]+)/contacts/activities%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_contacts_activities'), name="api_contacts_activities"),
        ]

    def avatar_upload(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        if profile.parent.user != request.user:
            return

        file = request.FILES['file']

        old_file_path = profile.parent.mugshot.path
        profile.parent.mugshot = file
        profile.parent.save()

        if os.path.isfile(old_file_path):
            os.remove(old_file_path)

        return self.create_response(request, {
            'avatar': profile.parent.mugshot.url,
        })

    def get_profile_activities(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        activities = []
        favoriteTags = {}
        followedTags = []
        for activity in ObjectProfileLink.objects.filter(profile=profile.parent, isValidated=True).order_by('-created_on'):
            obj = activity.content_object
            if activity.content_type.model == 'taggeditem':
                if obj.tag.slug in favoriteTags:
                    favoriteTags[obj.tag.slug] += 1
                else:
                    favoriteTags[obj.tag.slug] = 1
            elif activity.content_type == 'tag':
                followedTags.push(obj)
            else:
                activities.append({
                    'description' : render_to_string('notifications/activity.html', {'activity': activity, 'egocentric':True}),
                    'created_on' : activity.created_on
                })

        return self.create_response(request, {
            'objects': {'activities' : activities},
        })

    def get_contacts_activities(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        profile = MakerScienceProfile.objects.get(slug=kwargs["slug"])

        contact_ids = profile.parent.objectprofilelink_set.filter(level=40).values_list('object_id', flat=True) #Must return IDs of MakerScienceProfile
        contact_ids = MakerScienceProfile.objects.filter(id__in=[int(i) for i in contact_ids]).values_list('parent__id', flat=True)

        activities = []
        for activity in ObjectProfileLink.objects.filter(profile__in=contact_ids, isValidated=True).order_by('-created_on'):
            activities.append({
                'description' : render_to_string('notifications/activity.html', {'activity': activity, 'egocentric':False}),
                'created_on' : activity.created_on
            })

        return self.create_response(request, {
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
