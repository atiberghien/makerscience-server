from django.core.urlresolvers import reverse

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.paginator import Paginator
from haystack.query import SQ

from haystack.query import SearchQuerySet
from haystack.inputs import Raw
from graffiti.api import TagResource


from .models import MakerScienceStaticContent

import json

class MakerScienceStaticContentResource(ModelResource):
    project_thematic_selection = fields.ToManyField(TagResource, 'project_thematic_selection', full=True, null=True, readonly=True)
    resource_thematic_selection = fields.ToManyField(TagResource, 'resource_thematic_selection', full=True, null=True, readonly=True)

    class Meta:
        queryset = MakerScienceStaticContent.objects.all()
        allowed_methods = ['get', ]
        resource_name = 'makerscience/static'
        always_return_data = True


class SearchableMakerScienceResource(object):

    def prepare_result(self, request, sqs, limit):
        uri = reverse('api_ms_search', kwargs={'api_name':self.api_name,'resource_name': self._meta.resource_name})

        paginator = Paginator(request.GET, sqs, resource_uri=uri, limit=limit)

        objects = []
        for result in paginator.page()['objects']:
            if result:
                try:
                    bundle = self.build_bundle(obj=result.object, request=request)
                    bundle = self.full_dehydrate(bundle)
                    objects.append(bundle)
                except:
                    pass
        return {
            'meta': paginator.page()['meta'],
            'objects': objects,
        }

    def ms_advanced_search(self, request, **kwargs):
        get_params = request.GET.copy()
        limit = get_params.get('limit', self._meta.limit)

        sqs = SearchQuerySet().models(self.Meta.object_class).facet('tags')

        allWords = get_params.get('allWords', "").split(',')
        exactExpressions = get_params.get('exactExpressions', "").split(',')
        noneWord = get_params.get('noneWord', "").split(',')

        allWords = [] if allWords == [''] else allWords
        exactExpressions = [] if exactExpressions == [''] else exactExpressions
        noneWord = [] if noneWord == [''] else noneWord


        if get_params['searchIn'] in ['all', 'titles']:
            for term in allWords:
                print "allWords filter", term
                sqs = sqs.filter_and(text=term.strip())

            for term in exactExpressions:
                print "exactExpression filter", term
                sqs = sqs.filter_and(text=term.strip())

            for term in noneWord:
                print "noneWord filter", term
                sqs = sqs.exclude(text=term.strip())

        elif get_params['searchIn'] == 'tags':
            for term in allWords:
                sqs = sqs.filter_and(tags=term.strip())

            for term in exactExpressions:
                sqs = sqs.filter_and(tags=term.strip())

            for term in noneWord:
                sqs = sqs.exclude(tags=term.strip())

        self.log_throttled_access(request)
        return self.create_response(request, self.prepare_result(request, sqs, limit))

    def ms_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        get_params = request.GET.copy()

        if "advanced" in get_params:
            return self.ms_advanced_search(request, **kwargs)

        # Query params
        query = get_params.get('q', None)
        selected_facets = [item for sublist in [f.split(',') for f in get_params.getlist('facet', "")] for item in sublist]
        selected_facets = None if selected_facets == [''] else selected_facets

        ordering = get_params.get('ordering', None)
        limit = get_params.get('limit', self._meta.limit)

        for word in ["q", "facet", "ordering", "format", 'limit', 'offset']:
            if word in get_params.keys():
                try:
                    del get_params[word]
                except KeyError:
                    print word, "not in request"

        filtering = {}
        for key, val in get_params.iteritems():
            filtering[key] = json.loads(val)

        sqs = SearchQuerySet().models(self.Meta.object_class).facet('tags')

        if selected_facets:
            first_narrow_succes = False
            for i, facet in enumerate(selected_facets):
                tmp_sqs = sqs.narrow('tags:%s' % (facet))
                if len(tmp_sqs) :
                    first_narrow_succes = True
                if first_narrow_succes or i == len(selected_facets) - 1:
                    sqs = tmp_sqs
        if query:
            sqs = sqs.filter(text=Raw(query))
        if filtering :
            sqs = sqs.filter(**filtering)
        if ordering:
            sqs = sqs.order_by(ordering)


        self.log_throttled_access(request)
        return self.create_response(request, self.prepare_result(request, sqs, limit))
