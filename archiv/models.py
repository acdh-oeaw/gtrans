import re
import reversion

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from idprovider.models import IdProvider
from vocabs.models import SkosConcept
from entities.models import Person, Place, Institution
from browsing.browsing_utils import model_to_dict
from images.models import Image


@reversion.register()
class ArchResource(IdProvider):

    """ Beschreibt eine (archivalische) Resource """

    title = models.CharField(
        max_length=500, blank=True, verbose_name="Titel des Dokuments",
        help_text="Titel des Dokuments"
    )
    archiv = models.ForeignKey(
        Institution, null=True, blank=True,
        verbose_name="Archiv",
        help_text="Archiv in dem das Dokument aufbewahrt wird",
        related_name="has_docs_archived",
        on_delete=models.SET_NULL
    )
    signature = models.TextField(
        blank=True, verbose_name="(Archiv)Signatur",
        help_text="(Archiv)Signatur"
    )
    written_date = models.CharField(
        max_length=250, blank=True, verbose_name="Datum original",
        help_text="Datum original"
    )
    not_before = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Nicht vor normalisiert",
        help_text="YYYY-MM-DD"
    )
    not_after = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Nicht nach normalisiert",
        help_text="YYYY-MM-DD"
    )
    res_type = models.ForeignKey(
        SkosConcept, null=True, blank=True, verbose_name="Typ des Dokuments",
        help_text="Typ des Dokuments.",
        related_name="doc_type",
        on_delete=models.SET_NULL
    )
    subject_norm = models.ManyToManyField(
        SkosConcept, blank=True,
        help_text="Schlagwörter normalisiert",
        verbose_name="Schlagwörter normalisiert",
        related_name="subject_norm_of"
    )
    subject_free = models.TextField(
        blank=True, null=True, verbose_name="Schlagwörter original",
        help_text="Schlagwörter original"
    )
    abstract = models.TextField(
        blank=True, null=True, verbose_name="Zusammenfassung",
        help_text="Zusammenfassung"
    )
    notes = models.TextField(
        blank=True, null=True, verbose_name="Anmerkungen",
        help_text="Anmerkungen"
    )
    creator_person = models.ManyToManyField(
        Person, blank=True,
        help_text="Erzeuger des Dokuments",
        verbose_name="Erzeuger des Dokuments(Person)",
        related_name="created_by_person"
    )
    creator_inst = models.ManyToManyField(
        Institution, blank=True,
        help_text="Erzeuger des Dokuments(Institution)",
        verbose_name="Erzeuger des Dokuments(Institution)",
        related_name="created_by_inst"
    )
    mentioned_person = models.ManyToManyField(
        Person, blank=True,
        help_text="Im Dokument erwähnte Person",
        verbose_name="Im Dokument erwähnte Person",
        related_name="pers_mentioned_in_res"
    )
    mentioned_inst = models.ManyToManyField(
        Institution, blank=True,
        help_text="Im Dokument erwähnte Institution",
        verbose_name="Im Dokument erwähnte Institution",
        related_name="inst_mentioned_in_res"
    )
    mentioned_place = models.ManyToManyField(
        Place, blank=True,
        help_text="Im Dokument erwähnte Orte",
        verbose_name="Im Dokument erwähnte Orte",
        related_name="place_mentioned_in_res"
    )
    rel_res = models.ManyToManyField(
        'ArchResource', blank=True,
        help_text="In Verbindung stehende Dokumente",
        verbose_name="In Verbindung stehende Dokumente",
        related_name="related_res"
    )
    permalink = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="Permalink",
        help_text="Stabiler Link zu einem Digitalisat dieser Resource"
    )
    image = models.ManyToManyField(
        Image, blank=True,
        verbose_name="Faksimiles",
        help_text="Faksimiles",
        related_name="shows_document"
    )
    creators = models.ManyToManyField(
        User, blank=True,
        verbose_name="Verantwortlich",
        help_text="Verantwortlich für die Erzeugung dieses Datensatzes",
        related_name="created_archres"
    )

    def __str__(self):
        if self.title:
            return "Titel: {}".format(self.title)[:250]
        elif self.signature:
            return "Signatur: {}".format(self.signature)
        else:
            return "ID: {}".format(self.id)

    @classmethod
    def get_listview_url(self):
        return reverse('archiv:archresource_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:archresource_create')

    def get_absolute_url(self):
        return reverse('archiv:archresource_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('archiv:archresource_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('archiv:archresource_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'archiv:archresource_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'archiv:archresource_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def copy_instance(self):
        """Saves a copy of the current object and returns it"""
        obj = self
        obj.id = None
        obj.save()
        return obj

    def field_dict(self):
        return model_to_dict(self)
