from datetime import datetime
from django.conf.urls import url
from django.core.urlresolvers import reverse

from haystack.query import SearchQuerySet
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS

from dataserver.authentication import AnonymousApiKeyAuthentication
from accounts.api import ProfileResource
from scout.api import PlaceResource
from graffiti.api import TaggedItemResource

from makerscience_admin.api import SearchableMakerScienceResource
from .models import MakerScienceProfile, MakerScienceProfileTaggedItem

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
        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
        ]

class MakerScienceProfileTaggedItemResource(TaggedItemResource):

    class Meta:
        queryset = MakerScienceProfileTaggedItem.objects.all()
        resource_name = 'makerscience/profiletaggeditem'
        # authentication = AnonymousApiKeyAuthentication()
        # authorization = DjangoAuthorization()
        default_format = "application/json"
        filtering = {
            "tag" : ALL_WITH_RELATIONS,
            "object_id" : ['exact', ],
            'tag_type' : ['exact', ]
        }
        always_return_data = True
