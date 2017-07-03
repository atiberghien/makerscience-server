from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Q, Avg

from scout.models import Place
from projects.models import Project
from projectsheet.models import ProjectSheet
from accounts.models import ObjectProfileLink
from megafon.models import Post
from starlet.models import Vote
from taggit.models import TaggedItem

from makerscience_profile.models import MakerScienceProfile
from makerscience_catalog.models import MakerScienceProject, MakerScienceResource

class Command(BaseCommand):
    help = "Clear MakerScience"

    def handle(self, *args, **options):

        # in some obscure cases, content_object become None and crash
        print "Clearing ObjectProfileLink ...",
        for o in ObjectProfileLink.objects.all():
            if o.content_object == None or o.profile == None:
                o.delete()
        print "[OK]"

        print "Clearing ProjectSheet bucket ...",
        for p in ProjectSheet.objects.all():
            if p.bucket == None:
                #will raise signal pre_save createProjectSheetBucket on projectsheet (defined in dataserver.projectsheet.models)
                p.save()
        print "[OK]"

        print "Clearing MakerScienceProfile website ...",
        for p in MakerScienceProfile.objects.exclude(Q(website__startswith="http://") | Q(website__startswith="https://"))\
                                            .exclude(Q(website__isnull=True) | Q(website="")):
                p.website = "http://"+p.website
                p.save()
        print "[OK]"

        print "Clearing Project website ...",
        for p in Project.objects.exclude(Q(website__startswith="http://") | Q(website__startswith="https://"))\
                                            .exclude(Q(website__isnull=True) | Q(website="")):
                p.website = "http://"+p.website
                p.save()
        print "[OK]"

        print "Clearing Place ...",
        for p in Place.objects.all():
            if p.makerscienceprofile_set.count() == 0 and p.project_set.count() == 0:
                p.delete()
            else:
                p.address.save()
        print "[OK]"

        print "Clearing orphan TaggedItem ...",
        for t in TaggedItem.objects.all():
            if t.content_object == None or  t.tag == None:
                t.delete()
        print "[OK]"

        print "Clearing text-less post ...",
        for p in Post.objects.filter(text='', title__isnull=False):
            p.text = p.title
            p.save()
        print "[OK]"

        print "Update profile activity score...",
        for p in MakerScienceProfile.objects.all():
            p.activity_score = p.parent.objectprofilelink_set.all().count()
            p.save()
        print "[OK]"

        print "Update total_score"
        for p in MakerScienceProject.objects.all():
            votes = Vote.objects.filter(content_type=ContentType.objects.get_for_model(p), object_id=p.id)
            p.total_score = votes.aggregate(Avg('score'))['score__avg'] or 0.0
            p.save()
        for r in MakerScienceResource.objects.all():
            votes = Vote.objects.filter(content_type=ContentType.objects.get_for_model(r), object_id=r.id)
            r.total_score = votes.aggregate(Avg('score'))['score__avg'] or 0.0
            r.save()
