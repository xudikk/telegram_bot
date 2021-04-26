from os import path
from django.db import models
from django.db.models import JSONField
from django.conf import settings
from ..base.fields import lang_dict_field
from ..geo.models import Region, District

def logo_image_folder(instance, filename):
    return path.join("company", 'logo', filename)

class Statuses(models.Model):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.alias

class Companies(models.Model):
    company_name = models.CharField(max_length=150, blank=True, null=True, )
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True, )
    description = models.CharField(max_length=800, blank=True, null=True, )
    phone_number = models.CharField(max_length=20, blank=True, null=True, )
    logo = models.ImageField(upload_to=logo_image_folder, null=True, blank=True)
    lat = models.DecimalField("Latitude", max_digits=18, decimal_places=12, blank=True, null=True)
    lng = models.DecimalField("Longitude", max_digits=18, decimal_places=12, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True, )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="user_company",
        on_delete=models.SET_NULL,
    )
    region = models.ForeignKey(
        Region, related_name='company_region', null=True, blank=True,
        on_delete=models.SET_NULL)

    district = models.ForeignKey(
        District, related_name='company_district', null=True, blank=True,
        on_delete=models.SET_NULL)

    status = models.ForeignKey(
        Statuses,
        blank=True,
        null=True,
        related_name="status_company",
        on_delete=models.SET_NULL,
    )
    is_terms = models.BooleanField(default=False, null=False)
    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"

    def __str__(self):
        return self.company_name
