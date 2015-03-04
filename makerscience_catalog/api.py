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

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle

class MakerScienceResourceResource(ModelResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    tags = fields.ToManyField(TaggedItemResource, 'tagged_items', full=True, null=True)

    base_resourcesheet = fields.ToOneField(ProjectSheetResource, 'parent__projectsheet', null=True, full=True)

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

    def hydrate(self, bundle):
        bundle.data["modified"] = datetime.now()
        return bundle
