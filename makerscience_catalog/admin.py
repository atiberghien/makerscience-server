from django.contrib import admin
from .models import MakerScienceProject
from django.contrib.admin.options import ModelAdmin

admin.site.register(MakerScienceProject, ModelAdmin)