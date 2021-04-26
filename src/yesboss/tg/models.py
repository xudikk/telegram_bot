from django.db import models
from ..user.models import Types

class Users(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False,)
    user_type = models.ForeignKey(
        Types,
        blank=True,
        null=True,
        related_name="type_tg_user",
        on_delete=models.SET_NULL,
    )
    username = models.CharField(max_length=255, blank=True, null=True, )
    first_name = models.CharField(max_length=255, blank=True, null=True, )
    last_name = models.CharField(max_length=255, blank=True, null=True, )
    phone_number = models.CharField(max_length=20, blank=True, null=True, )
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)
    lang = models.SmallIntegerField(null=True, )

    def __str__(self):
        return "#%d" % self.user_id

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Telegram Users"

class Log(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False,)
    messages = models.JSONField(blank=True, null=True, )

    def __str__(self):
        return "#%s" % self.user_id

class Channel(models.Model):
    username = models.CharField(max_length=200, blank=False, null=False)
    token = models.CharField(max_length=400, blank=False, null=False)
    vacancy_channel_link = models.CharField(max_length=200, blank=False, null=False)
    vacancy_channel_id = models.CharField(max_length=200, blank=False, null=False)
    resume_channel_link = models.CharField(max_length=400, blank=False, null=False)
    resume_channel_id = models.CharField(max_length=400, blank=False, null=False)

    def __str__(self):
        return self.username
