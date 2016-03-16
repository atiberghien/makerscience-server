from django.core.management.base import BaseCommand
from django.db.models import Q
from optparse import make_option
from accounts.models import ObjectProfileLink
from scout.models import Place
from projectsheet.models import ProjectSheet
from makerscience_profile.models import MakerScienceProfile

class Command(BaseCommand):
    help = "Clear MakerScience"

    def handle(self, *args, **options):

        #in some obscure cases, content_object become None and crash
        print "Clearing ObjectProfileLink ...",
        for o in ObjectProfileLink.objects.all():
            if o.content_object == None or o.profile == None:
                # print "Clearing : %s (%s) - %s " % (o.profile.get_full_name_or_username(), o.profile.user.email, o.level)
                o.delete()
        print "[OK]"

        print "Clearing ProjectSheet bucket ...",
        for p in ProjectSheet.objects.all():
            if p.bucket == None:
                #will raise signal pre_save createProjectSheetBucket on projectsheet (defined in dataserver.projectsheet.models)
                p.save()
        print "[OK]"

        print "Clearing MakerScienceProfile website ...",
        for p in MakerScienceProfile.objects.exclude(Q(website__startswith="http://") | Q(website__startswith="http://"))\
                                            .exclude(Q(website__isnull=True) | Q(website="")):
                p.website = "http://"+p.website
                p.save()
        print "[OK]"

        print "Clearing Place ...",
        for p in Place.objects.all():
            if p.makerscienceprofile_set.count() == 0:
                p.delete()
            else:
                p.address.save()
        print "[OK]"
