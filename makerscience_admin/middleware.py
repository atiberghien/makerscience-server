from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import resolve

from .models import PageViews

from ipware.ip import get_real_ip, get_ip

import json


class PageViewsMiddleware(object):

    def process_response(self, request, response):
        if request.method == 'GET':
            try:
                view, args, kwargs = resolve(request.path)
                resource_name = kwargs.get("resource_name", None)
            except:
                resource_name = None

            if resource_name :
                if resource_name in settings.PAGEVIEWS_FILTER:
                    pageviews_counter = 0
                    content = json.loads(response.content)
                    if 'objects' in content and len(content['objects']) == 1:
                        resource_uri = content['objects'][0]['resource_uri']
                        created = False
                        autorepare = True #sometimes doublons can be created, don't know why
                        while autorepare:
                            autorepare = False
                            if request.user.is_authenticated() :
                                try:
                                    pv, created = PageViews.objects.get_or_create(client=request.user.username, resource_uri=resource_uri)
                                except PageViews.MultipleObjectsReturned:
                                    pv = PageViews.objects.filter(client=request.user.username, resource_uri=resource_uri)
                                    PageViews.objects.exclude(id=pv[0].id).delete()
                                    autorepare = True
                            else:
                                try:
                                    pv, created = PageViews.objects.get_or_create(client=get_ip(request), resource_uri=resource_uri)
                                except PageViews.MultipleObjectsReturned:
                                    pv = PageViews.objects.filter(client=get_ip(request), resource_uri=resource_uri)
                                    PageViews.objects.exclude(id=pv[0].id).delete()
                                    autorepare = True

                        pageviews_counter = PageViews.objects.filter(resource_uri=resource_uri).count()
                        content['objects'][0]['pageviews_counter'] = pageviews_counter
                        return HttpResponse(json.dumps(content), content_type="application/json")

        return response
