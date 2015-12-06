# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.options import ModelAdmin
from django.conf import settings
from django import forms

from mptt.admin import MPTTModelAdmin
from solo.admin import SingletonModelAdmin
from redactor.widgets import RedactorEditor
from taggit.models import Tag, TaggedItem

from makerscience_profile.models import MakerScienceProfile
from makerscience_catalog.models import MakerScienceProject, MakerScienceResource
from makerscience_forum.models import MakerSciencePost
from accounts.models import Profile, ObjectProfileLink
from megafon.models import Post
from .models import MakerScienceStaticContent, PageViews


# admin_registry = admin.site._registry.copy()
# for model, model_admin in admin_registry.iteritems():
#     admin.site.unregister(model)

class MakerScienceStaticContentForm(forms.ModelForm):
    class Meta:
        model = MakerScienceStaticContent
        widgets = {
            'about': RedactorEditor(),
            'about_howitworks': RedactorEditor(),
            'about_team': RedactorEditor(),
            'about_contact': RedactorEditor(),
            'about_faq': RedactorEditor(),
            'about_cgu': RedactorEditor(),
            'mentions': RedactorEditor(),
        }

class MakerScienceStaticContentAdmin(SingletonModelAdmin):
    form = MakerScienceStaticContentForm
    filter_horizontal = ("project_thematic_selection", 'resource_thematic_selection')
    fieldsets = (
        ('A propos', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('about', 'about_howitworks', 'about_team', 'about_contact', 'about_faq', 'about_cgu', "mentions")
        }),
        ('Sélections thématiques', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('project_thematic_selection', 'resource_thematic_selection')
        }),
        ('Réseaux sociaux', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('facebook', 'twitter', 'linkedin', 'youtube')
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
        return "%s - %s" % (obj.level, dict(settings.OBJECTPROFILELINK_CHOICES)[obj.level])
    display_level.short_description = 'Type de relation'

    def display_profile(self, obj):
        return "%s (#%s)" % (obj.profile.get_full_name_or_username().title(), obj.profile.id)
    display_profile.short_description = 'Profile'

    def display_content_object(self, obj):
        if obj.content_type.model == 'makerscienceproject' and MakerScienceProject.objects.filter(parent=obj.content_object).exists():
            return 'Projet : %s' % obj.content_object.parent.title
        if obj.content_type.model == 'makerscienceproject' and MakerScienceProject.objects.filter(id=obj.content_object.id).exists():
            return 'Projet : %s' % obj.content_object.parent.title
        elif obj.content_type.model == 'makerscienceresource' and MakerScienceResource.objects.filter(id=obj.object_id).exists():
            return 'Experience : %s' % obj.content_object.parent.title
        elif obj.content_type.model == 'makersciencepost' and MakerSciencePost.objects.filter(parent=obj.content_object).exists():
            return "Discussion : %s" % obj.content_object.title
        elif obj.content_type.model == 'post' and Post.objects.filter(id=obj.object_id).exists():
            return "Réponse à la discussion : %s" % obj.content_object.get_root()
        elif obj.content_type.model == 'makerscienceprofile' and MakerScienceProfile.objects.filter(id=obj.content_object.id).exists():
            return "%s (#%s)" % (obj.content_object.parent.get_full_name_or_username().title(), obj.object_id)
        elif obj.content_type.model == 'tag' and Tag.objects.filter(id=obj.content_object.id).exists():
            return "Tag %s" % obj.content_object.slug
        elif obj.content_type.model == 'taggeditem' and TaggedItem.objects.filter(id=obj.content_object.id).exists():
            return "Tag %s sur %s" % (obj.content_object.tag.slug, obj.content_object.content_object)
        return "Inconnu : %s %s" % (obj.content_type, obj.object_id)
    display_content_object.short_description = 'Contenu lié'

    list_display = ('id', 'display_profile', 'display_level', 'display_content_object', 'isValidated', 'created_on')
    list_filter = (ObjectProfileLinkLevelFilter, 'isValidated')
    list_editable = ('isValidated', )
    readonly_fields = ('created_on',)
    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }

    fieldsets = (
        (None, {
            'fields': (('content_type', 'object_id'), ("profile", 'detail'),  ('level', 'isValidated', 'created_on'))
        }),
    )

admin.site.register(ObjectProfileLink, ObjectProfileLinkAdmin)


class PageViewsAdmin(admin.ModelAdmin):
    list_display = ('client', 'resource_uri')

admin.site.register(PageViews, PageViewsAdmin)


class PostAdmin(MPTTModelAdmin):
    list_display = ('id', 'title')

admin.site.register(Post, PostAdmin)
