from django import template

from makerscience_profile.models import MakerScienceProfile

register = template.Library()

@register.simple_tag
def get_profile_for_slug(profile_slug):
    return MakerScienceProfile.objects.get(slug=profile_slug)
