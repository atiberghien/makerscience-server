from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api

from scout.api import MapResource, TileLayerResource, DataLayerResource, MarkerResource, MarkerCategoryResource, PostalAddressResource
from accounts.api import UserResource, GroupResource, ProfileResource, ObjectProfileLinkResource
from bucket.api import BucketResource, BucketFileResource, BucketTagResource, BucketFileCommentResource
from graffiti.api import TagResource, TaggedItemResource
from ucomment.api import CommentResource
from megafon.api   import PostResource

from projects.api import ProjectResource, ProjectProgressResource, ProjectProgressRangeResource
from projectsheet.api import ProjectSheetResource, ProjectSheetTemplateResource, ProjectSheetQuestionAnswerResource, ProjectSheetQuestionResource

from makerscience_catalog.api import MakerScienceProjectResource, MakerScienceResourceResource
from makerscience_profile.api import MakerScienceProfileResource, MakerScienceProfileTaggedItemResource
from makerscience_admin.api import MakerScienceStaticContentResource
import bucket

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
api.register(ObjectProfileLinkResource())

# Bucket
api.register(BucketResource())
api.register(BucketTagResource())
api.register(BucketFileResource())
api.register(BucketFileCommentResource())

#Graffiti
api.register(TagResource())
api.register(TaggedItemResource())

#Ucomment
api.register(CommentResource())

# Projects
api.register(ProjectResource())
api.register(ProjectProgressRangeResource())
api.register(ProjectProgressResource())

# Project Sheets
api.register(ProjectSheetResource())
api.register(ProjectSheetTemplateResource())
api.register(ProjectSheetQuestionAnswerResource())
api.register(ProjectSheetQuestionResource())

# Megafon
api.register(PostResource())

#MakerScience Catalog
api.register(MakerScienceProjectResource())
api.register(MakerScienceResourceResource())
#MakerScience Profile
api.register(MakerScienceProfileResource())
api.register(MakerScienceProfileTaggedItemResource())

#MakerScience Admin
api.register(MakerScienceStaticContentResource())

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
    url(r'^bucket/', include('bucket.urls'))

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
