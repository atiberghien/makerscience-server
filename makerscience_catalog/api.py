import json

from django.contrib.contenttypes.models import ContentType
from django.conf.urls import patterns, url, include
from django.shortcuts import get_object_or_404

from dataserver.authentication import AnonymousApiKeyAuthentication
from dataserver.authorization import GuardianAuthorization
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


from .models import MakerScienceProject, MakerScienceResource
from makerscience_profile.api import MakerScienceProfileResource
from accounts.models import ObjectProfileLink, Profile
from projectsheet.models import ProjectSheet

#FIXME : needs heavy refactoring
class MakerScienceProjectAuthorization(GuardianAuthorization):
    def __init__(self):
        super(MakerScienceProjectAuthorization, self).__init__(
            create_permission_code="add_makerscienceproject",
            view_permission_code="view_makerscienceproject",
            update_permission_code="change_makerscienceproject",
            delete_permission_code="delete_makerscienceproject"
        )

    def read_detail(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone read detail 
        """
        return True

    def read_list(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone read list 
        """
        return object_list

class MakerScienceProjectResource(ModelResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    tags = fields.ToManyField(TaggedItemResource, 'tagged_items', full=True, null=True)

    base_projectsheet = fields.ToOneField(ProjectSheetResource, 'parent__projectsheet', null=True, full=True)

    linked_resources = fields.ToManyField('makerscience_catalog.api.MakerScienceResourceResource', 'linked_resources', full=True,null=True)

    class Meta:
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


    def prepend_urls(self):
        """
        URL override for when giving change perm to a user profile passed as parameter profile_id
        """
        return [
           url(r"^(?P<resource_name>%s)/(?P<ms_id>\d+)/assign%s$" % 
                (self._meta.resource_name, trailing_slash()),
                 self.wrap_view('ms_edit_assign'), name="api_ms_project_assign"),
        ]

    def dehydrate(self, bundle):
        try:
            link = ObjectProfileLink.objects.get(content_type=ContentType.objects.get_for_model(bundle.obj.parent),
                                                   object_id=bundle.obj.parent.id,
                                                   level=0)
            profile = link.profile.makerscienceprofile_set.all()[0]

            bundle.data["by"] = {
                'profile_id' : profile.id,
                'profile_email' : profile.parent.user.email,
                'full_name' : "%s %s" % (profile.parent.user.first_name, profile.parent.user.last_name)
            }
        except Exception, e:
            pass
        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

    #FIXME / DRY me out !
    def ms_edit_assign(self, request, **kwargs):
        """
        Method to assign edit permissions for a MSResource or MSProject 'ms_id' to
        a user with profile passed as POST parameter 'profile_id' 
        """
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)
       
        target_profile_id = json.loads(request.body)['profile_id']
        target_profile = get_object_or_404(Profile, pk=target_profile_id)
        target_object_id = kwargs['ms_id']
        
        if kwargs['resource_name'] == 'makerscience/resource':
            target_object = get_object_or_404(MakerScienceResource, pk=target_object_id)
            assign_perm("change_makerscienceresource", user_or_group=target_profile.user, obj=target_object)
        elif kwargs['resource_name'] == 'makerscience/project':
            target_object = get_object_or_404(MakerScienceProject, pk=target_object_id)
            assign_perm("change_makerscienceproject", user_or_group=target_profile.user, obj=target_object)
        
        return self.create_response(request, {'success': True})

class MakerScienceResourceAuthorization(GuardianAuthorization):
    def __init__(self):
        super(MakerScienceResourceAuthorization, self).__init__(
            create_permission_code="add_makerscienceresource",
            view_permission_code="view_makerscienceresource",
            update_permission_code="change_makerscienceresource",
            delete_permission_code="delete_makerscienceresource"
        )

    def read_detail(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone read detail 
        """
        return True

    def read_list(self, object_list, bundle):
        """
        For MakerScienceResources we let anyone read list 
        """
        return object_list

class MakerScienceResourceResource(ModelResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    tags = fields.ToManyField(TaggedItemResource, 'tagged_items', full=True, null=True)

    base_resourcesheet = fields.ToOneField(ProjectSheetResource, 'parent__projectsheet', null=True, full=True)

    linked_resources = fields.ToManyField('makerscience_catalog.api.MakerScienceResourceResource', 'linked_resources', full=True,null=True)

    class Meta:
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

    def dehydrate(self, bundle):
        try:
            link = ObjectProfileLink.objects.get(content_type=ContentType.objects.get_for_model(bundle.obj.parent),
                                                   object_id=bundle.obj.parent.id,
                                                   level=0)
            profile = link.profile.makerscienceprofile_set.all()[0]

            bundle.data["by"] = {
                'profile_id' : profile.id,
                'profile_email' : profile.parent.user.email,
                'full_name' : "%s %s" % (profile.parent.user.first_name, profile.parent.user.last_name)
            }
        except Exception, e:
            pass
        return bundle

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

    def prepend_urls(self):
        """
        URL override for when giving change perm to a user profile passed as parameter profile_id
        """
        return [
           url(r"^(?P<resource_name>%s)/(?P<ms_id>\d+)/assign%s$" % 
                (self._meta.resource_name, trailing_slash()),
                 self.wrap_view('ms_edit_assign'), name="api_ms_resource_assign"),
        ]

    #FIXME / DRY me out !
    def ms_edit_assign(self, request, **kwargs):
        """
        Method to assign edit permissions for a MSResource or MSProject 'ms_id' to
        a user with profile passed as POST parameter 'profile_id' 
        """
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)
       
        target_profile_id = json.loads(request.body)['profile_id']
        target_profile = get_object_or_404(Profile, pk=target_profile_id)
        target_object_id = kwargs['ms_id']
        
        if kwargs['resource_name'] == 'makerscience/resource':
            target_object = get_object_or_404(MakerScienceResource, pk=target_object_id)
            assign_perm("change_makerscienceresource", user_or_group=target_profile.user, obj=target_object)
        elif kwargs['resource_name'] == 'makerscience/project':
            target_object = get_object_or_404(MakerScienceProject, pk=target_object_id)
            assign_perm("change_makerscienceproject", user_or_group=target_profile.user, obj=target_object)
        
        return self.create_response(request, {'success': True})


