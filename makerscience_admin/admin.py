from django.contrib import admin
from django import forms

from solo.admin import SingletonModelAdmin
from .models import MakerScienceStaticContent

from redactor.widgets import RedactorEditor

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



# from django.contrib.admin.options import ModelAdmin
#
# admin_registry = admin.site._registry.copy()
# for model, model_admin in admin_registry.iteritems():
#     admin.site.unregister(model)
#
# from makerscience_profile.models import MakerScienceProfile
# from makerscience_catalog.models import MakerScienceProject, MakerScienceResource
# from accounts.models import Profile, ObjectProfileLink
#
# from django.contrib.admin import SimpleListFilter
#
# class ObjectProfileLinkLevelFilter(SimpleListFilter):
#     title = 'Type de relation'
#     parameter_name = 'level'
#
#     def lookups(self, request, model_admin):
#         return (
#             (0, 'Equipe'),
#             (1, 'Ressource'),
#             (2, 'Fan'),
#         )
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(level=self.value())
#         return queryset
#
# class ObjectProfileLinkAdmin(admin.ModelAdmin):
#     def display_level(self, obj):
#         if obj.level == 0:
#             return 'Equipe'
#         elif obj.level == 1:
#             return 'Ressource'
#         elif obj.level == 2:
#             return 'Fan'
#     display_level.short_description = 'Type de relation'
#
#     def display_content_object(self, obj):
#         if MakerScienceProject.objects.filter(parent=obj.content_object).exists():
#             return 'Projet : %s' % obj.content_object.title
#         elif MakerScienceResource.objects.filter(parent=obj.content_object).exists():
#             return 'Experience : %s' % obj.content_object.title
#
#     list_display = ('profile', 'display_content_object', 'display_level', 'isValidated')
#     list_filter = (ObjectProfileLinkLevelFilter, 'isValidated')
#     list_editable = ('isValidated', )
#
# admin.site.register(ObjectProfileLink, ObjectProfileLinkAdmin)
