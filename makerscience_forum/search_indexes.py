from haystack import indexes
from taggit.models import Tag
from .models import MakerSciencePost


class MakerSciencePostIndex(indexes.SearchIndex, indexes.Indexable):

  text = indexes.EdgeNgramField(document=True, use_template=True)
  tags = indexes.MultiValueField(null=True, faceted=True)
  posted_on = indexes.DateTimeField(model_attr='parent__posted_on')
  updated_on = indexes.DateTimeField(model_attr='parent__updated_on')
  answers_count = indexes.IntegerField(model_attr='parent__answers_count')

  def get_model(self):
      return MakerSciencePost

  def prepare_tags(self, obj):
      return [tag.slug for tag in obj.parent.tags.all()]
