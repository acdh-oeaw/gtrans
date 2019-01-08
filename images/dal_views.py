from dal import autocomplete
from .models import Image
from django.db.models import Q


class ImageAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Image.objects.all()

        if self.q:
            qs = qs.filter(custom_filename__icontains=self.q)

        return qs
