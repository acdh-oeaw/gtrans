import re
from django.db import models
from django.urls import reverse
from idprovider.models import IdProvider

from browsing.browsing_utils import model_to_dict


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
        max_length=50, blank=True,
        help_text="GND-ID"
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
            return None
        except Exception as e:
            return None

    def save(self, *args, **kwargs):
        if self.geonames_id:
            new_id = self.get_geonames_url()
            self.geonames_id = new_id
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

    def __str__(self):
        return "{}".format(self.name)


class Institution(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(max_length=300, blank=True)
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
        verbose_name="Hauptstandort"
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
    authority_url = models.CharField(max_length=300, blank=True)
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
        next = self.__class__.objects.filter(id__gt=self.id)
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
