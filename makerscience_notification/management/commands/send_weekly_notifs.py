from django.core.management.base import BaseCommand

from makerscience_notification.models import send_notifications_by_mail

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        send_notifications_by_mail('WEEKLY')
