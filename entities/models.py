import re
import lxml.etree as ET
from django.db import models
from django.urls import reverse
from django.conf import settings
from idprovider.models import IdProvider
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

from browsing.browsing_utils import model_to_dict

from . utils import get_coordinates
from tei.entities_utils import person_to_tei, org_to_tei, place_to_tei

ARCHE_BASE_URL = getattr(settings, 'ARCHE_BASE_URL', 'https://id.acdh.oeaw.ac.at/MYPROJECT')


INSTITUTION_TYPES = (
    ('Partei', 'Partei'),
    ('Archiv', 'Archiv'),
    ('Sonstiges', 'Sonstiges'),
)


class Place(IdProvider):
    """Holds information about entities."""
    PLACE_TYPES = (
        ("city", "city"),
        ("country", "country")
    )
    name = models.CharField(
        max_length=250, blank=True, help_text="Normalized name"
    )
    alt_names = models.TextField(
        blank=True, verbose_name="Alternative Bezeichnungen",
        help_text="Im Falle mehrerer Einträge, diese bitte mit ';' trennen"
    )
    geonames_id = models.CharField(
        max_length=500, blank=True,
        verbose_name="Geonames-ID",
        help_text="z.B.: http://www.geonames.org/2773493/bad-kreuzen.html"
    )
    lat = models.DecimalField(
        max_digits=20, decimal_places=12,
        blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=20, decimal_places=12, blank=True, null=True
    )
    part_of = models.ForeignKey(
        "Place", null=True, blank=True,
        help_text="A place (country) this place is part of.",
        related_name="has_child",
        on_delete=models.SET_NULL
    )
    place_type = models.CharField(
        choices=PLACE_TYPES, null=True, blank=True, max_length=50
    )

    def get_geonames_url(self):
        if self.geonames_id.startswith('ht') and self.geonames_id.endswith('.html'):
            return self.geonames_id
        else:
            return "http://www.geonames.org/{}".format(self.geonames_id)

    def get_geonames_rdf(self):
        try:
            number = re.findall(r'\d+', str(self.geonames_id))[0]
            return number
        except Exception as e:
            return None

    def get_canonic_rdf(self):
        if self.get_geonames_rdf() is not None:
            can_uri = f"http://sws.geonames.org/{self.get_geonames_rdf()}/"
        else:
            can_uri = None
        return can_uri
    
    def arche_id(self):
        if self.get_canonic_rdf() is not None:
            return get_normalized_uri(f"{self.get_canonic_rdf()}")
        else:
            return f"{ARCHE_BASE_URL}/place/{self.id}"

    def save(self, *args, **kwargs):
        if self.geonames_id:
            new_id = self.get_geonames_url()
            self.geonames_id = new_id
        if self.get_geonames_rdf() and not self.lat:
            coords = get_coordinates(self.get_geonames_rdf())
            if coords:
                self.lat = coords['lat']
                self.lng = coords['lng']
        super(Place, self).save(*args, **kwargs)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:place_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:place_create')

    def get_absolute_url(self):
        return reverse('entities:place_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:place_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:place_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'entities:place_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:place_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def as_tei_node(self):
        return place_to_tei(self)

    def as_tei(self):
        return ET.tostring(self.as_tei_node(), pretty_print=True, encoding='UTF-8')

    def __str__(self):
        return "{}".format(self.name)


class Institution(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(
        verbose_name="Name",
        max_length=300, blank=True
    )
    authority_url = models.CharField(max_length=300, blank=True)
    alt_names = models.TextField(
        blank=True, verbose_name="Alternative Bezeichnungen",
        help_text="Im Falle mehrerer Einträge, diese bitte mit ';' trennen"
    )
    abbreviation = models.CharField(
        max_length=300, blank=True, verbose_name="Abkürzung"
    )
    location = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name="Hauptstandort", related_name="location_of_institution"
    )
    parent_institution = models.ForeignKey(
        'Institution', blank=True, null=True, related_name='children_institutions',
        on_delete=models.SET_NULL, verbose_name="Teil von Institution",
        help_text="provide some"
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name="Anmerkung, Kommentar",
        help_text="provide some"
    )
    institution_type = models.CharField(
        max_length=300, blank=True, verbose_name='Art der Institution',
        help_text="Partei, Archiv, sonstiges", choices=INSTITUTION_TYPES, default="Sonstiges"
    )

    def as_tei_node(self):
        return org_to_tei(self)

    def as_tei(self):
        return ET.tostring(self.as_tei_node(), pretty_print=True, encoding='UTF-8')

    @classmethod
    def get_listview_url(self):
        return reverse('entities:institution_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:institution_create')

    def get_absolute_url(self):
        return reverse('entities:institution_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:institution_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:institution_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'entities:institution_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:institution_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def __str__(self):
        return "{}".format(self.written_name)


class Person(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(
        max_length=300, blank=True
    )
    forename = models.CharField(
        max_length=300, blank=True,
        verbose_name="Vorname"
    )
    name = models.CharField(
        max_length=300, blank=True,
        verbose_name="Nachname"
    )
    acad_title = models.CharField(
        verbose_name="Akademische Titel",
        max_length=300, blank=True
    )
    alt_names = models.TextField(
        blank=True, verbose_name="Alternative Bezeichnungen",
        help_text="Im Falle mehrerer Einträge, diese bitte mit ';' trennen"
    )
    belongs_to_institution = models.ManyToManyField(
        Institution, blank=True,
        related_name="has_member",
    )
    belongs_to_party = models.ForeignKey(
        Institution, blank=True, null=True, related_name="has_party_member",
        on_delete=models.SET_NULL
    )
    place_of_birth = models.ForeignKey(
        Place, blank=True, null=True, related_name="is_birthplace",
        verbose_name="Geburtsort",
        on_delete=models.SET_NULL
    )
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Geburtsdatum",
        help_text="YYYY-MM-DD"
    )
    date_of_birth_written = models.CharField(
        verbose_name="ungefähres Geburtsdatum",
        max_length=300, blank=True
    )
    place_of_death = models.ForeignKey(
        Place, blank=True, null=True,
        verbose_name="Todesort",
        related_name="is_deathplace",
        on_delete=models.SET_NULL
    )
    date_of_death = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Todesdatum",
        help_text="YYYY-MM-DD"
    )
    date_of_death_written = models.CharField(
        verbose_name="ungefähres Sterbedatum",
        max_length=300, blank=True
    )
    authority_url = models.CharField(
        max_length=300, blank=True,
        verbose_name="GND-URL (oder Wikipedia)",
        help_text="https://portal.dnb.de/ oder https://de.wikipedia.org/"
    )
    comment = models.TextField(blank=True, null=True)
    biography = models.TextField(
        blank=True, null=True, verbose_name="biographische Anmerkungen",
        help_text="Weitere biographische Anmerkungen zur Person"
    )
    funktion = models.TextField(
        blank=True, null=True, verbose_name="Funktion",
        help_text="Funktionen, Tätigkeiten, Ämter"
    )
    quelle = models.TextField(
        blank=True, null=True, verbose_name="Quellen",
        help_text="Quellen"
    )
    type_of_person = models.CharField(
        max_length=300, blank=True, verbose_name='Art der Person',
        help_text="provide some"
    )

    class Meta:
        ordering = ['name']
    
    def arche_id(self):
        if "d-nb.info/gnd/" in self.authority_url:
            return get_normalized_uri(self.authority_url)
        else:
            return get_normalized_uri(f"{ARCHE_BASE_URL}/person/{self.id}")

    def as_tei_node(self):
        return person_to_tei(self)

    def as_tei(self):
        return ET.tostring(self.as_tei_node(), pretty_print=True, encoding='UTF-8')

    @classmethod
    def get_listview_url(self):
        return reverse('entities:person_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:person_create')

    def get_absolute_url(self):
        return reverse('entities:person_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('entities:person_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:person_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:person_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'entities:person_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:person_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def __str__(self):
        if self.written_name:
            return "{}".format(self.written_name)
        elif self.name and self.forename:
            return "{}, {}".format(self.name, self.forename)
        elif self.name:
            return "{}".format(self.name)
        else:
            return "No name provided"
