from django.db import models
from django.db.models import JSONField
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


from ..base.fields import lang_dict_field
from ..base.phonenumber_field.modelfields import PhoneNumberField
from ..base.utils.generator import create_tabnumber

class Types(models.Model):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.alias


class Statuses(models.Model):
    name = JSONField(blank=False, null=False, default=lang_dict_field)
    alias = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.alias

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_staff=False,
                    is_active=True, **extra_fields):
        'Creates a User with the given username, email and password'
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=is_active,
                          is_staff=is_staff, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_user_tg(self, tg_id, phone_number, first_name, user_type, lang):
        user = self.model(nickname=first_name, password=make_password(str(tg_id)),
                          types_id=user_type, first_name=None, tg_id=tg_id, status_id=1, lang=lang)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True,
                                is_superuser=True, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField( max_length=30, unique=True, blank=True, null=True, )
    nickname = models.CharField(max_length=200, blank=False, null=False, )
    first_name = models.CharField(max_length=70, blank=True, null=True, )
    last_name = models.CharField(max_length=70, blank=True, null=False, )
    user_type = models.SmallIntegerField(default=1)

    tab_number = models.IntegerField(null=False, blank=False,)
    tg_id = models.BigIntegerField(null=True, blank=True,)
    is_staff = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, )
    lang = models.SmallIntegerField(default=1, )
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    limit_credit = models.IntegerField(null=True, blank=True)
    types = models.ForeignKey(
        Types, on_delete=models.CASCADE,
        related_name="user_types", null=True, blank=True,
    )
    is_terms = models.BooleanField(default=False, null=False)
    status = models.ForeignKey(
        Statuses, on_delete=models.CASCADE,
        related_name="user_statuses", null=True, blank=True,
    )

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname or self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]
        get_latest_by = "date_joined"

    def save(self, *args, **kwargs):
        if self.tab_number is None or self.tab_number == "":
            self.tab_number = create_tabnumber(self)
        super(Users, self).save(*args, **kwargs)

class AuthUser(object):


    def checkpassword(self, password, encoded):
        return check_password(password, encoded)

class Contacts(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        related_name="contacts",
        on_delete=models.CASCADE,
    )
    phone_number = PhoneNumberField( max_length=30, blank=False, null=False, )
    is_active = models.BooleanField(default=True, )
    created_dt = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, editable=False)

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["-created_dt"]
        get_latest_by = "created_dt"

