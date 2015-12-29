from django import template

from makerscience_profile.models import MakerScienceProfile

register = template.Library()

@register.simple_tag
def get_profile_name_for_slug(profile_slug):
    return MakerScienceProfile.objects.get(slug=profile_slug).parent.get_full_name_or_username()
