from django.core.management.base import BaseCommand
from accounts.models import Account

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Account.objects.filter(username="parkashsatiyaar").exists():
            Account.objects.create_superuser(first_name="parkash", last_name="satiyaar", username="parkashsatiyaar", email="parkashsatiyaar0008@gmail", password="Parkash0008@")
