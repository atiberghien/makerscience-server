from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from optparse import make_option
from accounts.models import ObjectProfileLink
from projectsheet.models import ProjectSheet


class Command(BaseCommand):
    help = "Clear MakerScience"

    def handle(self, *args, **options):

        #in some obscure cases, content_object become None and crash
        for o in ObjectProfileLink.objects.all():
            if o.content_object == None or o.profile == None:
                print "Clearing : %s (%s) - %s " % (o.profile.get_full_name_or_username(), o.profile.user.email, o.level)
                o.delete()

        for p in ProjectSheet.objects.all():
            if p.bucket == None:
                #will raise signal pre_save createProjectSheetBucket on projectsheet (defined in dataserver.projectsheet.models)
                p.save()
