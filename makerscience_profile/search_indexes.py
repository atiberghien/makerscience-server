import datetime

from haystack import indexes
from taggit.models import Tag
from .models import MakerScienceProfile


class MakerScienceProfileIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField(null=True, faceted=True)
    date_joined = indexes.BooleanField(model_attr='parent__user__date_joined')
    activity_score = indexes.IntegerField()

    def get_model(self):
      return MakerScienceProfile

    def prepare_tags(self, obj):
      return [tag.name for tag in obj.tags.all()]

    def prepare_activity_score(self, obj):
        return obj.parent.objectprofilelink_set.all().count()
