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
from projects.api import ProjectResource, ProjectNewsResource
from projectsheet.api import ProjectSheetResource
from projects.models  import Project, ProjectNews


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
from bucket.api import BucketFileResource

class MakerScienceCatalogResource(ModelResource, SearchableMakerScienceResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    base_projectsheet = fields.ToOneField(ProjectSheetResource, 'parent__projectsheet', null=True, full=True)
    #CAN NOT BE a "LIGHT" resource BECAUSE "LIGHT" model doesn't exist
    linked_resources = fields.ToManyField('makerscience_catalog.api.MakerScienceResourceResource', 'linked_resources', full=True,null=True)
    linked_makersciencepost = fields.ToManyField('makerscience_forum.api.MakerSciencePostResourceLight', 'makersciencepost_set', full=True,null=True)

    def dehydrate_author(self, bundle):
        try:
            authoring_links = ObjectProfileLink.objects.filter(content_type=ContentType.objects.get_for_model(self._meta.object_class),
                                                                        isValidated=True,
                                                                          object_id=bundle.obj.id,
                                                                          level=self._meta.object_profile_link_level).order_by('created_on')
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

    def dehydrate(self, bundle):

        change_perm_code = "makerscience_catalog.change_%s" % bundle.obj._meta.model_name
        bundle.data["can_edit"] = bundle.request.user.has_perm(change_perm_code, bundle.obj)

        votes = Vote.objects.filter(content_type=ContentType.objects.get_for_model(self._meta.object_class), object_id=bundle.obj.id)
        bundle.data["total_score"] = votes.aggregate(Sum('score'))['score__sum'] or 0

        bundle = self.dehydrate_author(bundle)

        bundle.data["news"] = []
        for news in bundle.obj.parent.projectnews_set.all().order_by('-timestamp'):
            news_resource = ProjectNewsResource()
            news_bundle = news_resource.build_bundle(obj=news, request=bundle.request)
            news_bundle = news_resource.full_dehydrate(news_bundle)
            bundle.data["news"].append(news_bundle)

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
            url(r"^(?P<resource_name>%s)/publish/news%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('publish_news'), name="publish_news"),
        ]

    def publish_news(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)

        news_data = json.loads(request.body)
        news_data["author"] = Profile.objects.get(id=news_data["author"])
        news_data["project"] = Project.objects.get(id=news_data["project"])

        news = ProjectNews.objects.create(**news_data)
        news_resource = ProjectNewsResource()
        bundle = news_resource.build_bundle(obj=news, request=request)
        bundle = news_resource.full_dehydrate(bundle)
        return self.create_response(request, bundle)

class MakerScienceProjectAuthorization(MakerScienceAPIAuthorization):
    def __init__(self):
        super(MakerScienceProjectAuthorization, self).__init__(
            create_permission_code="makerscience_catalog.add_makerscienceproject",
            view_permission_code="makerscience_catalog.view_makerscienceproject",
            update_permission_code="makerscience_catalog.change_makerscienceproject",
            delete_permission_code="makerscience_catalog.delete_makerscienceproject"
        )

class MakerScienceProjectResourceLight(MakerScienceCatalogResource):
    parent_id = fields.IntegerField('parent__id')
    slug = fields.CharField('parent__slug')
    title = fields.CharField('parent__title')
    baseline = fields.CharField('parent__baseline', null=True)
    cover = fields.CharField('parent__projectsheet__cover__thumbnail_url', null=True)

    class Meta:
        object_class = MakerScienceProject
        object_profile_link_level = 0
        queryset = MakerScienceProject.objects.all()
        allowed_methods = ['get']
        resource_name = 'makerscience/projectlight'
        always_return_data = True
        excludes = ["parent", "base_projectsheet", "question_answers", "linked_resources"]
        filtering = {
            'parent_id' : ['exact'],
            'id' : ['exact'],
        }

    def dehydrate(self, bundle):
        return self.dehydrate_author(bundle)

class MakerScienceResourceResourceLight(MakerScienceCatalogResource):
    parent_id = fields.IntegerField('parent__id')
    slug = fields.CharField('parent__slug')
    title = fields.CharField('parent__title')
    baseline = fields.CharField('parent__baseline', null=True)
    cover = fields.CharField('parent__projectsheet__cover__thumbnail_url', null=True)

    class Meta:
        object_class = MakerScienceResource
        object_profile_link_level = 10
        queryset = MakerScienceResource.objects.all()
        allowed_methods = ['get']
        resource_name = 'makerscience/resourcelight'
        always_return_data = True
        excludes = ["parent", "base_projectsheet", "question_answers", "linked_resources"]
        filtering = {
            'parent_id' : ['exact'],
            'id' : ['exact'],
        }

    def dehydrate(self, bundle):
        return self.dehydrate_author(bundle)

class MakerScienceProjectResource(MakerScienceCatalogResource):
    tags = fields.ToManyField('makerscience_catalog.api.MakerScienceProjectTaggedItemResource', 'tagged_items', full=True, null=True, readonly=True)

    class Meta:
        object_class = MakerScienceProject
        object_profile_link_level = 0
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
        object_profile_link_level = 10
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
