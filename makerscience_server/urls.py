from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api

from scout.api import MapResource, TileLayerResource, DataLayerResource, MarkerResource, MarkerCategoryResource, PostalAddressResource
from accounts.api import UserResource, GroupResource, ProfileResource
from bucket.api import BucketResource, BucketFileResource, BucketTagResource, BucketFileCommentResource
from graffiti.api import TagResource, TaggedItemResource, ContentTypeResource


from projects.api import ProjectResource
from projectsheet.api import ProjectSheetResource, ProjectSheetTemplateResource, ProjectSheetSuggestedItemResource, ProjectSheetQuestionResource

from makerscience_catalog.api import MakerScienceProjectResource
from makerscience_profile.api import MakerScienceProfileResource

admin.autodiscover()

# Build API
api = Api(api_name='v0')

# Scout
api.register(MapResource())
api.register(TileLayerResource())
api.register(MarkerResource())
api.register(DataLayerResource())
api.register(MarkerCategoryResource())
api.register(PostalAddressResource())


# Auth
api.register(UserResource())
api.register(GroupResource())
api.register(ProfileResource())

# Bucket
api.register(BucketResource())
api.register(BucketTagResource())
api.register(BucketFileResource())
api.register(BucketFileCommentResource())

#Graffiti
api.register(TagResource())
api.register(TaggedItemResource())
api.register(ContentTypeResource())
# Projects
api.register(ProjectResource())

# Project Sheets
api.register(ProjectSheetResource())
api.register(ProjectSheetTemplateResource())
api.register(ProjectSheetSuggestedItemResource())
api.register(ProjectSheetQuestionResource())

#MakerScience Catalog
api.register(MakerScienceProjectResource())

#MakerScience Profile
api.register(MakerScienceProfileResource())


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)