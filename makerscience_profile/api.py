from .models import MakerScienceProfile
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS
from dataserver.authentication import AnonymousApiKeyAuthentication
from accounts.api import ProfileResource

class MakerScienceProfileResource(ModelResource):
    parent = fields.OneToOneField(ProfileResource, 'parent')
    
    class Meta:
        queryset = MakerScienceProfile.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'makerscience/profile'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = { 
            'parent' : ALL_WITH_RELATIONS,
        }