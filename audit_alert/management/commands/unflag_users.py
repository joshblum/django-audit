from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from audit_alert.models import FlaggedUser


class Command(BaseCommand):
    args = '<username username ...>'
    help = 'Unflag users of the specified usernames'

    def handle(self, *args, **options):
        self.stdout.write('Starting...\n')
        for username in args:
            try:
                user = User.objects.get(username=username)
                flags = FlaggedUser.objects.filter(user=user, flagged=True)
                for flag in flags:
                    flag.flagged=False
                    flag.save()
                self.stdout.write('Cleared %d flags for user: %s \n'% (len(flags), username))

            except User.DoesNotExist:
                self.stdout.write('User "%s" does not exist \n' % username)
        self.stdout.write('Done \n')




            
