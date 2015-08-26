import json

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf.urls import patterns, url, include
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from dataserver.authentication import AnonymousApiKeyAuthentication
from datetime import datetime
from graffiti.api import TaggedItemResource
from guardian.shortcuts import assign_perm, get_objects_for_user
from projects.api import ProjectResource
from projectsheet.api import ProjectSheetResource


from taggit.models import Tag
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from makerscience_admin.api import SearchableMakerScienceResource
from .models import MakerScienceProject, MakerScienceResource, MakerScienceProjectTaggedItem, MakerScienceResourceTaggedItem
from makerscience_server.authorizations  import  MakerScienceAPIAuthorization
from accounts.models import ObjectProfileLink, Profile
from projectsheet.models import ProjectSheet
from starlet.models import Vote

class MakerScienceCatalogResource(ModelResource, SearchableMakerScienceResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    base_projectsheet = fields.ToOneField(ProjectSheetResource, 'parent__projectsheet', null=True, full=True)
    linked_resources = fields.ToManyField('makerscience_catalog.api.MakerScienceResourceResource', 'linked_resources', full=True,null=True)

    def dehydrate_author(self, bundle):
        """Author is not a resource field. It must be add in bundle data. The entry must be called 'by' """
        raise Exception("Must be implemented by sub class")

    def dehydrate(self, bundle):

        change_perm_code = "makerscience_catalog.change_%s" % bundle.obj._meta.model_name
        bundle.data["can_edit"] = bundle.request.user.has_perm(change_perm_code, bundle.obj)

        votes = Vote.objects.filter(content_type=ContentType.objects.get_for_model(self._meta.object_class), object_id=bundle.obj.id)
        bundle.data["total_score"] = votes.aggregate(Sum('score'))['score__sum'] or 0

        bundle = self.dehydrate_author(bundle)

        bundle.data["linked_post"] =[]
        for post_id in bundle.obj.makersciencepost_set.values_list('id', flat=True):
            bundle.data["linked_post"].append(post_id)

        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

    def prepend_urls(self):
        """
        URL override for permissions and search specials
        """
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ms_search'), name="api_ms_search"),
        ]

class MakerScienceProjectAuthorization(MakerScienceAPIAuthorization):
    def __init__(self):
        super(MakerScienceProjectAuthorization, self).__init__(
            create_permission_code="makerscience_catalog.add_makerscienceproject",
            view_permission_code="makerscience_catalog.view_makerscienceproject",
            update_permission_code="makerscience_catalog.change_makerscienceproject",
            delete_permission_code="makerscience_catalog.delete_makerscienceproject"
        )

class MakerScienceProjectResource(MakerScienceCatalogResource):
    tags = fields.ToManyField('makerscience_catalog.api.MakerScienceProjectTaggedItemResource', 'tagged_items', full=True, null=True, readonly=True)

    class Meta:
        object_class = MakerScienceProject
        queryset = MakerScienceProject.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/project'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MakerScienceProjectAuthorization()
        always_return_data = True
        filtering = {
            'parent' : ALL_WITH_RELATIONS,
            'featured' : ['exact'],
        }
        limit = 6

    def dehydrate_author(self, bundle):
        try:
            authoring_links = ObjectProfileLink.objects.filter(content_type=ContentType.objects.get_for_model(MakerScienceProject),
                                                                        isValidated=True,
                                                                          object_id=bundle.obj.id,
                                                                          level=0).order_by('created_on')
            profile = authoring_links[0].profile.makerscienceprofile_set.all()[0]

            bundle.data["by"] = {
                'profile_slug' : profile.slug,
                'profile_id' : profile.id,
                'profile_email' : profile.parent.user.email,
                'full_name' : profile.parent.get_full_name_or_username()
            }
        except :
            bundle.data["by"] = {
                'profile_slug' : "",
                'profile_id' : "",
                'profile_email' : "",
                'full_name' : ""
            }
        return bundle

class MakerScienceResourceAuthorization(MakerScienceAPIAuthorization):
    def __init__(self):
        super(MakerScienceResourceAuthorization, self).__init__(
            create_permission_code="makerscience_catalog.add_makerscienceresource",
            view_permission_code="makerscience_catalog.view_makerscienceresource",
            update_permission_code="makerscience_catalog.change_makerscienceresource",
            delete_permission_code="makerscience_catalog.delete_makerscienceresource"
        )

class MakerScienceResourceResource(MakerScienceCatalogResource):
    tags = fields.ToManyField('makerscience_catalog.api.MakerScienceResourceTaggedItemResource', 'tagged_items', full=True, null=True, readonly=True)

    class Meta:
        object_class = MakerScienceResource
        queryset = MakerScienceResource.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/resource'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MakerScienceResourceAuthorization()
        always_return_data = True
        filtering = {
            'parent' : ALL_WITH_RELATIONS,
            'featured' : ['exact'],
        }
        limit = 6

    def dehydrate_author(self, bundle):
        try:
            authoring_links = ObjectProfileLink.objects.filter(content_type=ContentType.objects.get_for_model(MakerScienceResource),
                                                                isValidated=True,
                                                                          object_id=bundle.obj.id,
                                                                          level=10).order_by('created_on')
            profile = authoring_links[0].profile.makerscienceprofile_set.all()[0]

            bundle.data["by"] = {
                'profile_slug' : profile.slug,
                'profile_id' : profile.id,
                'profile_email' : profile.parent.user.email,
                'full_name' : profile.parent.get_full_name_or_username()
            }
        except :
            bundle.data["by"] = {
                'profile_slug' : "",
                'profile_id' : "",
                'profile_email' : "",
                'full_name' : ""
            }
        return bundle

class MakerScienceProjectTaggedItemResource(TaggedItemResource):

    class Meta:
        queryset = MakerScienceProjectTaggedItem.objects.all()
        resource_name = 'makerscience/projecttaggeditem'
        default_format = "application/json"
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
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

class MakerScienceResourceTaggedItemResource(TaggedItemResource):

    class Meta:
        queryset = MakerScienceResourceTaggedItem.objects.all()
        resource_name = 'makerscience/resourcetaggeditem'
        default_format = "application/json"
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
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
