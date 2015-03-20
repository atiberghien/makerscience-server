from django.contrib import admin
from .models import MakerScienceProject, MakerScienceResource
from django.contrib.admin.options import ModelAdmin
from guardian.admin import GuardedModelAdmin

class MakerScienceProjectAdmin(GuardedModelAdmin):
    pass

class MakerScienceResourceAdmin(GuardedModelAdmin):
    pass
    
admin.site.register(MakerScienceProject, MakerScienceProjectAdmin)
admin.site.register(MakerScienceResource, MakerScienceResourceAdmin)
