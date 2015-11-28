from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum

from haystack import indexes
from taggit.models import Tag

from starlet.models import Vote

from .models import MakerScienceResource, MakerScienceProject

import datetime

class MakerScienceProjectIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    tags = indexes.MultiValueField(null=True, faceted=True)
    featured = indexes.BooleanField(model_attr='featured')
    created_on = indexes.DateTimeField(model_attr='parent__created_on')
    total_score = indexes.FloatField()

    def get_model(self):
      return MakerScienceProject

    def prepare_tags(self, obj):
        return [tag.slug for tag in obj.tags.all()]

    def prepare_total_score(self, obj):
        votes = Vote.objects.filter(content_type=ContentType.objects.get_for_model(self.get_model()),
                                    object_id=obj.id)
        return votes.aggregate(Sum('score'))['score__sum'] or 0.0

class MakerScienceResourceIndex(MakerScienceProjectIndex):

  def get_model(self):
      return MakerScienceResource
