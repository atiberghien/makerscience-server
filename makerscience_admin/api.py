from django.core.urlresolvers import reverse

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.paginator import Paginator

from haystack.query import SearchQuerySet
from haystack.inputs import Raw
from graffiti.api import TagResource


from .models import MakerScienceStaticContent

class MakerScienceStaticContentResource(ModelResource):
    project_thematic_selection = fields.ToManyField(TagResource, 'project_thematic_selection', full=True, null=True, readonly=True)
    resource_thematic_selection = fields.ToManyField(TagResource, 'resource_thematic_selection', full=True, null=True, readonly=True)

    class Meta:
        queryset = MakerScienceStaticContent.objects.all()
        allowed_methods = ['get', ]
        resource_name = 'makerscience/static'
        always_return_data = True


class SearchableMakerScienceResource(object):

    def ms_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        # Query params
        query = request.GET.get('q', '')
        selected_facets = [item for sublist in [f.split(',') for f in request.GET.getlist('facet', [])] for item in sublist]
        ordering = request.GET.get('ordering', None)

        sqs = SearchQuerySet().models(self.Meta.object_class).facet('tags')

        if selected_facets:
            first_narrow_succes = False
            for i, facet in enumerate(selected_facets):
                tmp_sqs = sqs.narrow('tags:%s' % (facet))
                if len(tmp_sqs) :
                    first_narrow_succes = True
                if first_narrow_succes or i == len(selected_facets) - 1:
                    sqs = tmp_sqs
        if query != "":
            sqs = sqs.filter(text=Raw(query))
        if ordering:
            sqs = sqs.order_by(ordering)


        uri = reverse('api_ms_search', kwargs={'api_name':self.api_name,'resource_name': self._meta.resource_name})
        paginator = Paginator(request.GET, sqs, resource_uri=uri, limit=self._meta.limit)

        objects = []
        for result in paginator.page()['objects']:
            if result:
                bundle = self.build_bundle(obj=result.object, request=request)
                bundle = self.full_dehydrate(bundle)
                objects.append(bundle)
        object_list = {
            'meta': paginator.page()['meta'],
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
