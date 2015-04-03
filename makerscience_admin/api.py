from .models import MakerScienceStaticContent
from tastypie.resources import ModelResource

class MakerScienceStaticContentResource(ModelResource):
    class Meta:
        queryset = MakerScienceStaticContent.objects.all()
        allowed_methods = ['get', ]
        resource_name = 'makerscience/static'
        always_return_data = True
