# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import MakerSciencePost
from django.contrib.admin.options import ModelAdmin
from guardian.admin import GuardedModelAdmin

class MakerSciencePostAdmin(GuardedModelAdmin):
    def display_title(self, obj):
        return obj.parent.title
    display_title.short_description = 'Titre'

    def display_date(self, obj):
        return obj.parent.posted_on
    display_date.short_description = 'Posté le'

    list_display = ('display_title', 'display_date', 'post_type')
    list_filter = ('parent__posted_on', 'post_type')
    pass

admin.site.register(MakerSciencePost, MakerSciencePostAdmin)
