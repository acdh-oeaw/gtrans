from django.db.models import Q
from dal import autocomplete
from . models import ArchResource


class ArchResourceAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ArchResource.objects.all()

        if self.q:
            qs = qs.filter(
                Q(id__icontains=self.q) |
                Q(title__icontains=self.q) |
                Q(signature__icontains=self.q)
            )
        return qs
