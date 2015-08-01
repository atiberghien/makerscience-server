from haystack import indexes
from taggit.models import Tag
from .models import MakerSciencePost


class MakerSciencePostIndex(indexes.SearchIndex, indexes.Indexable):

  text = indexes.CharField(document=True, use_template=True)
  tags = indexes.MultiValueField(null=True, faceted=True)
  updated_on = indexes.BooleanField(model_attr='parent__updated_on')
  answers_count = indexes.IntegerField(model_attr='parent__answers_count')

  def get_model(self):
      return MakerSciencePost

  def prepare_tags(self, obj):
      return [tag.name for tag in obj.parent.tags.all()]
