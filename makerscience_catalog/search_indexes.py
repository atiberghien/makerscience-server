import datetime

from haystack import indexes
from taggit.models import Tag
from .models import MakerScienceResource, MakerScienceProject


class MakerScienceProjectIndex(indexes.SearchIndex, indexes.Indexable):
    
  text = indexes.CharField(document=True, use_template=True)
  tags = indexes.MultiValueField(null=True, faceted=True)

  def get_model(self):
      return MakerScienceProject
  
  def prepare_tags(self, obj):
      return [tag.name for tag in obj.tags.all()]


class MakerScienceResourceIndex(MakerScienceProjectIndex):
    
  def get_model(self):
      return MakerScienceResource
