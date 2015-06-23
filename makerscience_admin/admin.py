# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.options import ModelAdmin
from django.conf import settings
from django import forms

from solo.admin import SingletonModelAdmin
from redactor.widgets import RedactorEditor


from makerscience_profile.models import MakerScienceProfile
from makerscience_catalog.models import MakerScienceProject, MakerScienceResource
from makerscience_forum.models import MakerSciencePost
from accounts.models import Profile, ObjectProfileLink
from .models import MakerScienceStaticContent, PageViews


# admin_registry = admin.site._registry.copy()
# for model, model_admin in admin_registry.iteritems():
#     admin.site.unregister(model)

class MakerScienceStaticContentForm(forms.ModelForm):
    class Meta:
        model = MakerScienceStaticContent
        widgets = {
            'about': RedactorEditor(),
            'about_team': RedactorEditor(),
            'about_contact': RedactorEditor(),
            'about_faq': RedactorEditor(),
            'about_cgu': RedactorEditor(),
        }

class MakerScienceStaticContentAdmin(SingletonModelAdmin):
    form = MakerScienceStaticContentForm

    fieldsets = (
        ('About', {
            'classes': ('collapse',),
            'fields': ('about', 'about_team', 'about_contact', 'about_faq', 'about_cgu')
        }),
    )


admin.site.register(MakerScienceStaticContent, MakerScienceStaticContentAdmin)

class ObjectProfileLinkLevelFilter(SimpleListFilter):
    title = 'Type de relation'
    parameter_name = 'level'

    def lookups(self, request, model_admin):
        return settings.OBJECTPROFILELINK_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(level=self.value())
        return queryset

class ObjectProfileLinkAdmin(admin.ModelAdmin):
    def display_level(self, obj):
        return dict(settings.OBJECTPROFILELINK_CHOICES)[obj.level]
    display_level.short_description = 'Type de relation'

    def display_content_object(self, obj):
        if MakerScienceProject.objects.filter(parent=obj.content_object).exists():
            return 'Projet : %s' % obj.content_object.title
        elif MakerScienceResource.objects.filter(parent=obj.content_object).exists():
            return 'Experience : %s' % obj.content_object.title
        elif MakerSciencePost.objects.filter(parent=obj.content_object).exists():
            return "Discussion : %s" % obj.content_object.title
    display_content_object.short_description = 'Contenu lié'

    list_display = ('profile', 'display_level', 'display_content_object', 'isValidated')
    list_filter = (ObjectProfileLinkLevelFilter, 'isValidated')
    list_editable = ('isValidated', )


admin.site.register(ObjectProfileLink, ObjectProfileLinkAdmin)


class PageViewsAdmin(admin.ModelAdmin):
    list_display = ('client', 'resource_uri')

admin.site.register(PageViews, PageViewsAdmin)
