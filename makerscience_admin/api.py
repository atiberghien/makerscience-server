from .models import MakerScienceStaticContent
from tastypie.resources import ModelResource

from django.core.urlresolvers import reverse

from haystack.query import SearchQuerySet
from tastypie.paginator import Paginator
from haystack.inputs import Raw

class MakerScienceStaticContentResource(ModelResource):
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
        selected_facets = request.GET.getlist('facet', None)
        ordering = request.GET.get('ordering', None)

        sqs = SearchQuerySet().models(self.Meta.object_class).facet('tags')

        if ordering:
            sqs = sqs.order_by(ordering)
        if selected_facets:
            for facet in selected_facets:
                sqs = sqs.narrow('tags:%s' % (facet))
        if query != "":
            sqs = sqs.filter(text=Raw(query))


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
