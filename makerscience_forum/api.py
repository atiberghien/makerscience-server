from django.conf.urls import url
from django.core.urlresolvers import reverse

from tastypie.resources import ModelResource
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.paginator import Paginator

from haystack.query import SearchQuerySet

from dataserver.authentication import AnonymousApiKeyAuthentication
from megafon.api  import PostResource

from makerscience_admin.api import SearchableMakerScienceResource
from makerscience_catalog.api import MakerScienceProjectResourceLight, MakerScienceResourceResourceLight
from makerscience_server.authorizations import MakerScienceAPIAuthorization
from .models import MakerSciencePost
from graffiti.api import TaggedItemResource


class MakerSciencePostAuthorization(MakerScienceAPIAuthorization):
    def __init__(self):
        super(MakerSciencePostAuthorization, self).__init__(
            create_permission_code="makerscience_forum.add_makersciencepost",
            view_permission_code="makerscience_forum.view_makersciencepost",
            update_permission_code="makerscience_forum.change_makersciencepost",
            delete_permission_code="makerscience_forum.delete_makersciencepost"
        )

class MakerSciencePostResourceLight(ModelResource, SearchableMakerScienceResource):
    slug = fields.CharField('parent__slug')
    parent_id = fields.IntegerField('parent__id')
    updated_on = fields.DateField('parent__updated_on')
    title = fields.CharField('parent__title')
    answers_count = fields.IntegerField('parent__answers_count')
    tags = fields.ToManyField(TaggedItemResource, 'parent__tagged_items', full=True, null=True)

    class Meta:
        queryset = MakerSciencePost.objects.all()
        allowed_methods = ['get']
        resource_name = 'makerscience/postlight'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MakerSciencePostAuthorization()
        always_return_data = True
        filtering = {
            'post_type' : ['exact'],
            'parent_id' : ['exact'],
            'id' : ['exact'],
        }

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
        ]


class MakerSciencePostResource(ModelResource, SearchableMakerScienceResource):
    parent = fields.ToOneField(PostResource, 'parent', full=True)

    linked_projects = fields.ToManyField(MakerScienceProjectResourceLight, 'linked_projects', full=True,null=True)
    linked_resources = fields.ToManyField(MakerScienceResourceResourceLight, 'linked_resources', full=True,null=True)

    class Meta:
        queryset = MakerSciencePost.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'makerscience/post'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MakerSciencePostAuthorization()
        always_return_data = True
        filtering = {
            'parent' : ALL_WITH_RELATIONS,
            'post_type' : ['exact'],
            'linked_projects' : ['isnull']
        }
        limit = 7

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
        ]
