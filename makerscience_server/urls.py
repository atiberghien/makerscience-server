from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api

from scout.api import PlaceResource #MapResource, TileLayerResource, DataLayerResource, MarkerResource, MarkerCategoryResource, PostalAddressResource
from accounts.api import UserResource, GroupResource, ProfileResource, ObjectProfileLinkResource
from bucket.api import BucketResource, BucketFileResource, BucketTagResource, BucketFileCommentResource
from graffiti.api import TagResource, TaggedItemResource
from ucomment.api import CommentResource
from megafon.api   import PostResource
from starlet.api import VoteResource

from projects.api import ProjectResource, ProjectProgressResource, ProjectProgressRangeResource, ProjectNewsResource
from projectsheet.api import ProjectSheetResource, ProjectSheetTemplateResource, ProjectSheetQuestionAnswerResource, ProjectSheetQuestionResource

from makerscience_catalog.api import MakerScienceProjectResource, MakerScienceResourceResource, MakerScienceProjectTaggedItemResource, MakerScienceResourceTaggedItemResource, MakerScienceProjectResourceLight, MakerScienceResourceResourceLight
from makerscience_profile.api import MakerScienceProfileResource, MakerScienceProfileResourceLight, MakerScienceProfileTaggedItemResource
from makerscience_forum.api import MakerSciencePostResource, MakerSciencePostResourceLight
from makerscience_admin.api import MakerScienceStaticContentResource
from makerscience_notification.api import NotificationResource
import bucket

admin.autodiscover()

# Build API
api = Api(api_name='v0')

# Scout
# api.register(MapResource())
# api.register(TileLayerResource())
# api.register(MarkerResource())
# api.register(DataLayerResource())
# api.register(MarkerCategoryResource())
# api.register(PostalAddressResource())
api.register(PlaceResource())

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

#Starlet
api.register(VoteResource())

# Projects
api.register(ProjectResource())
api.register(ProjectProgressRangeResource())
api.register(ProjectProgressResource())

# Project Sheets
api.register(ProjectSheetResource())
api.register(ProjectSheetTemplateResource())
api.register(ProjectSheetQuestionAnswerResource())
api.register(ProjectSheetQuestionResource())
api.register(ProjectNewsResource())

# Megafon
api.register(PostResource())

#MakerScience Catalog
api.register(MakerScienceProjectResource())
api.register(MakerScienceProjectResourceLight())
api.register(MakerScienceResourceResourceLight())
api.register(MakerScienceResourceResource())
api.register(MakerScienceProjectTaggedItemResource())
api.register(MakerScienceResourceTaggedItemResource())
#MakerScience Profile
api.register(MakerScienceProfileResource())
api.register(MakerScienceProfileResourceLight())
api.register(MakerScienceProfileTaggedItemResource())
#Makerscience Forum
api.register(MakerSciencePostResource())
api.register(MakerSciencePostResourceLight())
#MakerScience Admin
api.register(MakerScienceStaticContentResource())

#Makerscience Notification
api.register(NotificationResource())

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
    url(r'^bucket/', include('bucket.urls')),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
