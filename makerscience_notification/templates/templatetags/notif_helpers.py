from django import template

from makerscience_profile.models import MakerScienceProfile

register = template.Library()

@register.filter(name='profile_fullname')
def profile_fullname(value):
    return MakerScienceProfile.objects.get(slug=value).parent.get_full_name_or_username()
