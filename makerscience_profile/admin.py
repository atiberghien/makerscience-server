from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin.options import ModelAdmin

from guardian.admin import GuardedModelAdmin

from accounts.models import Profile
from .models import MakerScienceProfile

import csv

def export_email(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="membres_emails.csv"'

    writer = csv.writer(response)
    for member in queryset:
        writer.writerow([member.parent.user.first_name,
                         member.parent.user.last_name,
                         member.parent.user.email])
    return response
export_email.short_description = "Exporter les emails des membres en CSV"

class MakerScienceProfileAdmin(GuardedModelAdmin):
    search_fields = ['parent__user__first_name', 'parent__user__last_name','parent__user__email']
    actions = [export_email]

admin.site.register(MakerScienceProfile, MakerScienceProfileAdmin)
