from os import path
from datetime import datetime
from django.db import models
from django.db.models import JSONField
from django.conf import settings

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from mptt.managers import TreeManager

from ..base.fields import lang_dict_field
from ..base.models import SortableModel
from ..geo.models import Region, District
from ..company.models import Companies
from ..user.models import Contacts
from ..storing.models import Files

def get_file_folder(instance, filename):
    today = datetime.now()
    return path.join("hr", today.strftime("%Y"), today.strftime("%m"), filename)


class Statuses(models.Model):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name['ru']

class Languages(models.Model):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)
    sort_order = models.IntegerField(db_index=True, null=True)

    def __str__(self):
        return self.name['ru']

class Category(MPTTModel, SortableModel):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    slug = models.SlugField(unique=True, max_length=255)

    parent = TreeForeignKey('self', related_name='prcategorychildren', null=True, blank=True, on_delete=models.SET_NULL)

    objects = models.Manager()
    tree = TreeManager()
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False, null=False, db_index=True)

    def __str__(self):
        return self.name['ru']


    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def get_ordering_queryset(self):
        return Category.objects.all()

class Positions(SortableModel):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    slug = models.SlugField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, related_name='categorypostion', null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.name['ru']


    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def get_ordering_queryset(self):
        return Positions.objects.all()

def default_schdule_data():
    return {
        "uz": {"0": "Dushanba", "1": "Seshanba", "2": "Chorshanba", "3": "Payshanba", "4": "Juma"},
        "ru": {"0": "Понедельник", "1": "Вторник", "2": "Среда", "3": "Четверг", "4": "Пятница"}
    }

class Schedules(models.Model):
    def default_data(self=None):
        return {
            "uz": {"0": "Dushanba", "1": "Seshanba", "2": "Chorshanba", "3": "Payshanba", "4": "Juma"},
            "ru": {"0": "Понедельник", "1": "Вторник", "2": "Среда", "3": "Четверг", "4": "Пятница"}
        }

    data = JSONField(blank=False, null=False, default=default_schdule_data)
    name = JSONField(blank=True, null=True, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True, blank=True, null=True,)

    def __str__(self):
        return self.alias

def default_experience_val():
    return {"from": 0, "to": 0}

def default_salary():
    return {"from": 0, "to": 0}

def default_contacts():
    return {"mobile": "", "home": "", "office": ""}

def default_experience():
    return {"from": 0, "to": 0}

def default_languages():
    return {}

class Experience(models.Model):
    data = JSONField(blank=False, null=False, default=default_experience_val)
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)
    sort_order = models.IntegerField(db_index=True, null=True)

    def __str__(self):
        return self.alias

class Resume(models.Model):

    def default_subcats(self):
        return {"cats": []}

    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=30, blank=True, null=True, )
    lastname = models.CharField(max_length=33, blank=True, null=True, )
    middlename = models.CharField(max_length=40, blank=True, null=True, )
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="user_resumes",
        on_delete=models.SET_NULL,
    )

    schedule = models.ForeignKey(
        Schedules,
        blank=True,
        null=True,
        related_name="schedules_resume",
        on_delete=models.SET_NULL,
    )
    status = models.ForeignKey(
        Statuses,
        blank=True,
        null=True,
        related_name="status_resume",
        on_delete=models.SET_NULL,
    )

    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
        related_name="region_resume",
        on_delete=models.SET_NULL,
    )

    district = models.ForeignKey(
        District,
        blank=True,
        null=True,
        related_name="district_resume",
        on_delete=models.SET_NULL,
    )

    salary = JSONField(blank=True, null=False, default=default_salary)
    experience = models.ForeignKey(
        Experience,
        blank=True,
        null=True,
        related_name="schedules_experience",
        on_delete=models.SET_NULL,
    )
    languages = JSONField(blank=True, null=True)

    about = models.CharField(blank=True, max_length=600)
    views_count = models.IntegerField(default=0, editable=False)
    contact_count = models.IntegerField(default=0, editable=False)
    contact = models.ForeignKey(
        Contacts,
        blank=True,
        null=True,
        related_name="resume_contacts",
        on_delete=models.SET_NULL,
    )
    position_name = models.CharField(max_length=200, blank=True, null=True)
    files = models.ForeignKey(
        Files,
        blank=True,
        null=True,
        related_name="resume_files",
        on_delete=models.SET_NULL,
    )
    age = models.IntegerField(blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    skills = models.CharField(max_length=600, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    created_dt = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, editable=False)
    updated_dt = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, editable=False)

class ResumeCategories(models.Model):
    resume = models.ForeignKey(
        Resume,
        related_name="resume_categories_m",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    category = models.ForeignKey(
        Category,
        related_name="resume_categories",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = (('resume', 'category'),)


def vacancy_default_salary():
    return {"from": 0, "to": 0}

def vacancy_default_experience():
    return {"from": 0, "to": 0}

def vacancy_default_languages():
    return {}

def vacancy_default_contacts():
    return {"mobile": "", "home": "", "office": ""}

def vacancy_default_subcats():
    return {"cats": []}

class Vacancies(models.Model):



    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="user_vacancy",
        on_delete=models.SET_NULL,
    )
    company = models.ForeignKey(
        Companies,
        blank=True,
        null=True,
        related_name="company_vacancies",
        on_delete=models.SET_NULL,
    )
    schedule = models.ForeignKey(
        Schedules,
        blank=True,
        null=True,
        related_name="schedules_vacancies",
        on_delete=models.SET_NULL,
    )

    status = models.ForeignKey(
        Statuses,
        blank=True,
        null=True,
        related_name="status_vacancies",
        on_delete=models.SET_NULL,
    )

    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
        related_name="region_vacancies",
        on_delete=models.SET_NULL,
    )

    district = models.ForeignKey(
        District,
        blank=True,
        null=True,
        related_name="district_vacancies",
        on_delete=models.SET_NULL,
    )
    experience = models.ForeignKey(
        Experience,
        blank=True,
        null=True,
        related_name="experience_vacancies",
        on_delete=models.SET_NULL,
    )
    position = models.ForeignKey(
        Positions,
        blank=True,
        null=True,
        related_name="position_vacancies",
        on_delete=models.SET_NULL,
    )
    position_name = models.CharField(max_length=200, blank=True, null=True)
    file_type = models.SmallIntegerField(blank=True, null=True)
    # file_path = models.CharField(max_length=600, blank=True, null=True)
    file_path = models.FileField(upload_to=get_file_folder, max_length=300, blank=True, null=True)
    files = models.ForeignKey(
        Files,
        blank=True,
        null=True,
        related_name="vacancies_files",
        on_delete=models.SET_NULL,
    )
    salary = JSONField(blank=True, null=False, default=vacancy_default_salary)
    age = JSONField(blank=True, null=False, default=vacancy_default_experience)
    languages = JSONField(blank=True, null=True)

    requirements = models.CharField(blank=True, null=True, max_length=600)
    views_count = models.IntegerField(default=0, editable=False)
    contact_count = models.IntegerField(default=0, editable=False)
    gender = models.IntegerField(default=0, editable=False)

    created_dt = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, editable=False)
    updated_dt = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, editable=False)

class VacanciCategories(models.Model):
    vacancy = models.ForeignKey(
        Vacancies,
        related_name="vacancies_categories_v",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    category = models.ForeignKey(
        Category,
        related_name="vacancies_categories",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = (('vacancy', 'category'),)

class VacanciLanguage(models.Model):
    vacancy = models.ForeignKey(
        Vacancies,
        related_name="vacancies_language_v",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    language = models.ForeignKey(
        Languages,
        related_name="vacancies_language",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = (('vacancy', 'language'), )

class ResumeLanguage(models.Model):
    resume = models.ForeignKey(
        Resume,
        related_name="resume_language_v",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    language = models.ForeignKey(
        Languages,
        related_name="resume_language",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = (('resume', 'language'), )

