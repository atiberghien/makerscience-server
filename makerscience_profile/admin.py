from django.contrib import admin
from .models import MakerScienceProfile
from django.contrib.admin.options import ModelAdmin
from accounts.models import Profile
from guardian.admin import GuardedModelAdmin

admin.site.register(MakerScienceProfile, GuardedModelAdmin)
