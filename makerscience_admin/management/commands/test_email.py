from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from optparse import make_option

class Command(BaseCommand):
    help = "Test email backend."

    option_list = BaseCommand.option_list + (
        make_option('--email', '-e',
                    dest='email',
                    help='Email to send to'),
    )
    def handle(self, *args, **options):
        print "EMAIL", options['email']
        send_mail('Makerscience test email backend',
                  'Does it work ?',
                  'admin@makerscience.fr',
                   [options['email']],  fail_silently=False)
