from haystack import indexes
from taggit.models import Tag
from .models import MakerSciencePost


class MakerScienceProjectIndex(indexes.SearchIndex, indexes.Indexable):

  text = indexes.CharField(document=True, use_template=True)
  tags = indexes.MultiValueField(null=True, faceted=True)
  post_type = indexes.BooleanField(model_attr='post_type')

  def get_model(self):
      return MakerSciencePost

  def prepare_tags(self, obj):
      return [tag.name for tag in obj.parent.tags.all()]
