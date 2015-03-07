from django.contrib.contenttypes.models import ContentType

from dataserver.authentication import AnonymousApiKeyAuthentication
from datetime import datetime
from graffiti.api import TaggedItemResource
from projects.api import ProjectResource
from projectsheet.api import ProjectSheetResource

from taggit.models import Tag
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from .models import MakerScienceProject, MakerScienceResource
from makerscience_profile.api import MakerScienceProfileResource
from accounts.models import ObjectProfileLink
from projectsheet.models import ProjectSheet


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
        authorization = DjangoAuthorization()
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
        authorization = DjangoAuthorization()
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
