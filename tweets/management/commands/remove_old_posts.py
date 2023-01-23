from django.core.management.base import BaseCommand
from tweets.models import HackPost
from datetime import datetime, timedelta

class Command(BaseCommand):
    """
    Delete all unpublished posts older than 10 days.
    """
    help = "Delete all unpublished posts older than 10 days."

    def handle(self, *args, **options):
        HackPost.objects\
            .filter(published=False)\
            .filter(posting_date__lte=datetime.now()-timedelta(days=10)).delete()
        self.stdout.write('Deleted posts older than 10 days')
