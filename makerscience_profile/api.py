from .models import MakerScienceProfile, MakerScienceProfileTaggedItem
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS
from dataserver.authentication import AnonymousApiKeyAuthentication
from accounts.api import ProfileResource
from scout.api import PostalAddressResource
from projects.api import ProjectTeamResource
from graffiti.api import TaggedItemResource
from django.conf.urls import url
from tastypie.utils import trailing_slash
from datetime import datetime

class MakerScienceProfileResource(ModelResource):
    parent = fields.OneToOneField(ProfileResource, 'parent', full=True)
    location = fields.ToOneField(PostalAddressResource, 'location', null=True, blank=True, full=True)

    tags = fields.ToManyField('makerscience_profile.api.MakerScienceProfileTaggedItemResource', 'tagged_items', full=True, null=True, readonly=True)

    teams = fields.ToManyField(ProjectTeamResource, 'parent__projectteam_set', full=True, null=True, readonly=True)

    class Meta:
        queryset = MakerScienceProfile.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/profile'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'parent' : ALL_WITH_RELATIONS,
            "location" : ['isnull', ],
        }

    def dehydrate(self, bundle):
        bundle.data["full_name"] = "%s %s" % (bundle.obj.parent.user.first_name, bundle.obj.parent.user.last_name)
        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

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

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_id>\d+?)/(?P<tag_type>\w+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_id>\d+?)/similars%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('get_similars'),
               name="api_get_similars"),
        ]
