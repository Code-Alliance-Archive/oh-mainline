from django.core.management.base import BaseCommand

from mysite.profile.view_helpers import push_volunteer_changes_to_zoho_crm

class Command(BaseCommand):
    help = "Uploads information about new / edited volunteers to Zoho CRM."

    def handle(self, *args, **options):
        push_volunteer_changes_to_zoho_crm()
