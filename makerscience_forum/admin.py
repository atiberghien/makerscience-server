from django.contrib import admin
from .models import MakerSciencePost
from django.contrib.admin.options import ModelAdmin
from guardian.admin import GuardedModelAdmin

class MakerSciencePostAdmin(GuardedModelAdmin):
    pass

admin.site.register(MakerSciencePost, MakerSciencePostAdmin)
