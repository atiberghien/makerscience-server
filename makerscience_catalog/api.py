from .models import MakerScienceProject
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from projects.api import ProjectResource
from graffiti.api import TagResource
from taggit.models import Tag
from tastypie.constants import ALL_WITH_RELATIONS


class MakerScienceProjectResource(ModelResource):
    parent = fields.OneToOneField(ProjectResource, 'parent')
    tags = fields.ToManyField(TagResource, 'tags') 
    
    class Meta:
        queryset = MakerScienceProject.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/project'
        authorization = Authorization()
        always_return_data = True
        filtering = { 
            'parent' : ALL_WITH_RELATIONS,
        }

    def hydrate(self, bundle):
        tags_objects = []
        for tagName in bundle.data["tags"]:
            tags_objects.append(Tag.objects.get_or_create(name=tagName)[0])
        bundle.data["tags"] = tags_objects
        return bundle