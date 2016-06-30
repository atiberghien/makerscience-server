# -*- coding: utf-8 -*-

from urlparse import urlparse
import json
import urllib2

from django.http.response import HttpResponse
from lxml import html


def parse_html_img(request):
    """
    Parsing IMG src in HTML content
    """
    response_data = []

    if request.method == 'GET':
        url = request.GET.get('url', None)

        if url:
            if not url.startswith('http'):
                url = u"http://{}".format(url)

            response = urllib2.urlopen(url)
            content = response.read()
            tree = html.fromstring(content)
            imgs = tree.findall('.//img')

            for elt in imgs:
                src = elt.attrib.get(u'src', None)
                # alt is alt tag or filename
                alt = elt.attrib.get(u'alt', url.split('/')[-1])

                if src:
                    if src.startswith(u'//'):
                        # add current protocol
                        if url.startswith(u'http:'):
                            response_data.append({'src': u"http:{}".format(src),
                                                  'alt': alt})

                        elif url.startswith(u'https:'):
                            response_data.append({'src': u"https:{}".format(src),
                                                  'alt': alt})

                    elif src.startswith('/'):
                        # add current protocol and domain
                        parsed_uri = urlparse(url)
                        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                        response_data.append({'src': u"{}{}".format(domain, src[1:]),
                                              'alt': alt})

                    else:
                        # just add it
                        response_data.append({'src': src,
                                              'alt': alt})

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


def parse_url_link(request):
    """
    Parsing URL link
    """

    ALLOWED_EXTENSIONS = (
        # html / imgs / documents
        'text/html',
        'image/jpeg',
        'image/gif',
        'image/png',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )

    response_data = {}

    if request.method == 'GET':
        url = request.GET.get('url', None)
        if not url.startswith('http'):
            url = u"http://{}".format(url)

        if url:
            response = urllib2.urlopen(url)
            infos = response.info()

            if infos.type not in ALLOWED_EXTENSIONS:
                raise Exception(infos.type)

            elif infos.type == 'text/html':
                content = response.read()
                tree = html.fromstring(content)
                title_tag = tree.find('.//title')

                if title_tag is not None:
                    title = title_tag.text_content()

                else:
                    title = ""

                meta_description = ""

                try:
                    descriptions = tree.xpath("//meta[@name='description']/@content")

                    if not descriptions:
                        descriptions = tree.xpath("//meta[@property='og:description']/@content")

                        if not descriptions:
                            descriptions = tree.xpath("//meta[@property='twitter:description']/@content")

                    if descriptions:
                        meta_description = descriptions[0]

                except:
                    pass

                description = meta_description

            else:
                title = url.split('/')[-1]
                description = ""

            response_data = {'url': url,
                             'title': title.replace('_', ' '),
                             'description': description, }

    return HttpResponse(json.dumps(response_data),
                        mimetype='application/json')
