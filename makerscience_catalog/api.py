from dataserver.authentication import AnonymousApiKeyAuthentication
from datetime import datetime
from graffiti.api import TagResource
from projects.api import ProjectResource

from taggit.models import Tag
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from .models import MakerScienceProject, MakerScienceResource
from projectsheet.models import ProjectSheet


class MakerScienceProjectResource(ModelResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)
    
    class Meta:
        queryset = MakerScienceProject.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/project'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = { 
            'parent' : ALL_WITH_RELATIONS,
        }
        
    def hydrate(self, bundle):
        tags_objects = []
        for tagName in bundle.data["tags"]:
            tags_objects.append(Tag.objects.get_or_create(name=tagName)[0])
        bundle.data["tags"] = tags_objects
        bundle.data["modified"] = datetime.now()
        return bundle

    def dehydrate(self, bundle):
        bundle.data["template"] = ProjectSheet.objects.get(project=bundle.obj.parent).template
        return bundle
    
class MakerScienceResourceResource(ModelResource):
    parent = fields.ToOneField(ProjectResource, 'parent', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)
    
    class Meta:
        queryset = MakerScienceResource.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/resource'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = { 
            'parent' : ALL_WITH_RELATIONS,
        }
        
    def hydrate(self, bundle):
        tags_objects = []
        for tagName in bundle.data["tags"]:
            tags_objects.append(Tag.objects.get_or_create(name=tagName)[0])
        bundle.data["tags"] = tags_objects
        bundle.data["modified"] = datetime.now()
        return bundle

    def dehydrate(self, bundle):
        bundle.data["template"] = ProjectSheet.objects.get(project=bundle.obj.parent).template
        return bundle 