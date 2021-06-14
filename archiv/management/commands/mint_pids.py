from entities.models import ARCHE_BASE_URL
from django.core.management.base import BaseCommand
from django.conf import settings

from acdh_handle_pyutils.client import HandleClient

from archiv.models import ArchResource
from archeutils.utils import get_arche_id


USER = settings.HANDLE_USER
PW = settings.HANDLE_PASSWORD

class Command(BaseCommand):

    """mints handles for all `archiv.ArchResource` objects"""

    help = 'mints handles for all `archiv.ArchResource` objects'
    
    def handle(self, *args, **options):
        hdl_client = HandleClient(USER, PW)
        items = ArchResource.objects.exclude(pid__icontains="http")
        print(f"{items.count()} without PIDs found")
        for x in items:
            parsed_data = f"{get_arche_id(x)}"
            pid = hdl_client.register_handle(parsed_data)
            x.pid = pid
            x.save()
            print(pid, parsed_data)

