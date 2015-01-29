from django.contrib import admin
from .models import MakerScienceProject, MakerScienceResource
from django.contrib.admin.options import ModelAdmin

admin.site.register(MakerScienceProject, ModelAdmin)
admin.site.register(MakerScienceResource, ModelAdmin)
