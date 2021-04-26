from django.core.validators import MinLengthValidator
from django.db import models

class Country(models.Model):
    """ Model for the country of origin.
    """
    iso_code = models.CharField(max_length=2, unique=True, blank=False, null=True, db_index=True, default=None,
                                help_text='ISO 3166-1 alpha 2', validators=[MinLengthValidator(2)])

    iso_code3 = models.CharField(max_length=3, unique=True, blank=False, null=True, db_index=True, default=None,
                                 help_text='ISO 3166-1 alpha 3', validators=[MinLengthValidator(3)])

    name_ru = models.CharField(max_length=100, db_index=True, blank=False)

    name_uz = models.CharField(max_length=100, db_index=True, blank=False)

    lat = models.DecimalField("Latitude", max_digits=18, decimal_places=12, blank=True, null=True)

    lng = models.DecimalField("Longitude", max_digits=18, decimal_places=12, blank=True, null=True)

    class Meta:
        verbose_name_plural ='Countries'
        ordering = ['name_ru']

    def __unicode__(self):
        return u"%s (%s)" % (self.name_ru, self.iso_code)

    def clean(self):
        super(Country, self).clean()
        self.iso_code = self.iso_code.upper()
        self.iso_code3 = self.iso_code3.upper()

    def __str__(self):
        return self.name_ru


class Region(models.Model):

    name_ru = models.CharField(max_length=100, db_index=True, verbose_name="rus name")

    name_uz = models.CharField(max_length=100, db_index=True, verbose_name="uzb name")

    country = models.ForeignKey(Country, related_name="region_country", on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField(default=0)
    geo_position = models.CharField(max_length=100, null=True, blank=True,)

    def __unicode__(self):
        return self.name_ru

    def __str__(self):
        return self.name_ru

    @property
    def parent(self):
        return self.country

    def full_code(self):
        return ".".join([self.parent.code, self.name_ru])

class District(models.Model):

    name_ru = models.CharField(max_length=100, db_index=True, verbose_name="rus name")

    name_uz = models.CharField(max_length=100, db_index=True, verbose_name="name_uz")

    country = models.ForeignKey(Country, related_name="district_country", on_delete=models.CASCADE)

    region = models.ForeignKey(Region, related_name="district_region", on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField(default=0)
    geo_position = models.CharField(max_length=100, null=True, blank=True,)

    @property
    def parent(self):
        return self.region

    def __unicode__(self):
        return self.name_ru

    def __str__(self):
        return self.name_ru
