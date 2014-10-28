from .models import MakerScienceProject
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from projects.api import ProjectResource
from graffiti.api import TagResource


class MakerScienceProjectResource(ModelResource):
    parent = fields.OneToOneField(ProjectResource, 'parent')
    tags = fields.ToManyField(TagResource, 'tags') 
    
    class Meta:
        queryset = MakerScienceProject.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/project'
        authorization = Authorization()
        always_return_data = True
