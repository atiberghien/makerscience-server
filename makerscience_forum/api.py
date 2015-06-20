from django.conf.urls import url
from django.core.urlresolvers import reverse

from tastypie.resources import ModelResource
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.paginator import Paginator

from haystack.query import SearchQuerySet

from dataserver.authentication import AnonymousApiKeyAuthentication
from megafon.api  import PostResource

from makerscience_server.authorizations import MakerScienceAPIAuthorization
from .models import MakerSciencePost

class MakerSciencePostAuthorization(MakerScienceAPIAuthorization):
    def __init__(self):
        super(MakerSciencePostAuthorization, self).__init__(
            create_permission_code="makerscience_forum.add_makersciencepost",
            view_permission_code="makerscience_forum.view_makersciencepost",
            update_permission_code="makerscience_forum.change_makersciencepost",
            delete_permission_code="makerscience_forum.delete_makersciencepost"
        )

class MakerSciencePostResource(ModelResource):
    parent = fields.ToOneField(PostResource, 'parent', full=True)

    class Meta:
        queryset = MakerSciencePost.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'makerscience/post'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MakerSciencePostAuthorization()
        always_return_data = True
        filtering = {
            'parent' : ALL_WITH_RELATIONS,
            'post_type' : ['exact'],
        }

    def prepend_urls(self):
        """
        URL override for permissions and search specials
        """
        return [
           url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name,
                                trailing_slash()), self.wrap_view('ms_search'), name="api_ms_search"),
        ]

    def ms_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        # Query params
        query = request.GET.get('q', '')
        selected_facets = request.GET.getlist('facet', None)
        featured = request.GET.get('featured', '')

        sqs = SearchQuerySet().models(self.Meta.object_class).facet('tags')

        # narrow down QS with facets
        if selected_facets:
            for facet in selected_facets:
                sqs = sqs.narrow('tags:%s' % (facet))
        # launch query
        if query != "":
            sqs = sqs.auto_query(query)

        if featured != '':
            sqs =sqs.filter(featured=featured)

        uri = reverse('api_ms_search', kwargs={'api_name':self.api_name,'resource_name': self._meta.resource_name})
        paginator = Paginator(request.GET, sqs, resource_uri=uri)

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
