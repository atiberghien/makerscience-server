from django.contrib import admin
from .models import MakerScienceProfile
from django.contrib.admin.options import ModelAdmin
from accounts.models import Profile


admin.site.register(MakerScienceProfile, ModelAdmin)
