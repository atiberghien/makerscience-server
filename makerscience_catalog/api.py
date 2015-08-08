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

    def dehydrate(self, bundle):

        votes = Vote.objects.filter(content_type=ContentType.objects.get_for_model(self._meta.object_class), object_id=bundle.obj.id)
        bundle.data["total_score"] = votes.aggregate(Sum('score'))['score__sum'] or 0

        try:
            authoring_links = ObjectProfileLink.objects.filter(content_type=ContentType.objects.get_for_model(bundle.obj.parent),
                                                                object_id=bundle.obj.parent.id,
                                                                level__in=[0,10]).order_by('created_on')
            profile = authoring_links[0].profile.makerscienceprofile_set.all()[0]

            bundle.data["by"] = {
                'profile_slug' : profile.slug,
                'profile_id' : profile.id,
                'profile_email' : profile.parent.user.email,
                'full_name' : "%s %s" % (profile.parent.user.first_name, profile.parent.user.last_name)
            }
        except :
            bundle.data["by"] = {
                'profile_slug' : "",
                'profile_id' : "",
                'profile_email' : "",
                'full_name' : ""
            }

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
            url(r"^(?P<resource_name>%s)/(?P<ms_id>\d+)/assign%s$" %
                (self._meta.resource_name, trailing_slash()),
                 self.wrap_view('ms_edit_assign'), name="api_edit_assign"),
            url(r"^(?P<resource_name>%s)/(?P<ms_id>\d+)/check/(?P<user_id>\d+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                 self.wrap_view('ms_check_edit_perm'), name="api_ms_check_edit_perm"),
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ms_search'), name="api_ms_search"),
        ]


    #FIXME / DRY me out !
    def ms_edit_assign(self, request, **kwargs):
        """
        Method to assign edit permissions for a MSResource or MSProject 'ms_id' to
        a user with id passed as POST parameter 'user_id'
        """
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)

        target_user_id = json.loads(request.body)['user_id']
        target_user = get_object_or_404(User, pk=target_user_id)
        target_object_id = kwargs['ms_id']
        # FIXME : for better security, we should also check that request.user has edit rights on target object
        # => which implies that change rigths are automatically given to creator of a sheet
        target_object = get_object_or_404(self.Meta.object_class, pk=target_object_id)
        change_perm_code = self.Meta.authorization.update_permission_code
        assign_perm(change_perm_code, user_or_group=target_user, obj=target_object)

        return self.create_response(request, {'msg' : 'Change rights assigned'})

    def ms_check_edit_perm(self, request, **kwargs):
        """
        Method to check edit permissions for a given user_id
        """
        self.method_check(request, allowed=['get', 'post'])
        self.throttle_check(request)
        self.is_authenticated(request)

        user_id = kwargs['user_id']
        user = get_object_or_404(User, pk=user_id)

        target_object_id = kwargs['ms_id']
        target_object = get_object_or_404(self.Meta.object_class, pk=target_object_id)
        change_perm_code = self.Meta.authorization.update_permission_code
        if user.has_perm(change_perm_code, target_object):
            return self.create_response(request, {'has_perm':True})
        else:
            return self.create_response(request, {'has_perm':False})

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


class MakerScienceProjectTaggedItemResource(TaggedItemResource):

    class Meta:
        queryset = MakerScienceProjectTaggedItem.objects.all()
        resource_name = 'makerscience/projecttaggeditem'
        default_format = "application/json"
        filtering = {
            "tag" : ALL_WITH_RELATIONS,
            "object_id" : ['exact', ],
            'tag_type' : ['exact', ]
        }
        always_return_data = True
        limit = 0

class MakerScienceResourceTaggedItemResource(TaggedItemResource):

    class Meta:
        queryset = MakerScienceResourceTaggedItem.objects.all()
        resource_name = 'makerscience/resourcetaggeditem'
        default_format = "application/json"
        filtering = {
            "tag" : ALL_WITH_RELATIONS,
            "object_id" : ['exact', ],
            'tag_type' : ['exact', ]
        }
        always_return_data = True
        limit = 0
