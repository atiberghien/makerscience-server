from django.contrib import admin
from .models import MakerScienceProject, MakerScienceResource
from django.contrib.admin.options import ModelAdmin
from guardian.admin import GuardedModelAdmin

class MakerScienceProjectAdmin(GuardedModelAdmin):
    list_display = ('parent', 'featured')
    list_editable = ('featured', )

class MakerScienceResourceAdmin(GuardedModelAdmin):
    list_display = ('parent', 'featured')
    list_editable = ('featured', )

admin.site.register(MakerScienceProject, MakerScienceProjectAdmin)
admin.site.register(MakerScienceResource, MakerScienceResourceAdmin)
