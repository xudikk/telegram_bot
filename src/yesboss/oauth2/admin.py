from django.contrib import admin

from .models import (AccessToken, Application, Grant, RefreshToken)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "client_type", "authorization_grant_type")
    list_filter = ("client_type", "authorization_grant_type", "skip_authorization")
    radio_fields = {
        "client_type": admin.HORIZONTAL,
        "authorization_grant_type": admin.VERTICAL,
    }
    raw_id_fields = ("user", )


class GrantAdmin(admin.ModelAdmin):
    list_display = ("code", "application", "user", "expires")
    raw_id_fields = ("user", )


class AccessTokenAdmin(admin.ModelAdmin):
    search_fields = ['user__id']
    list_display = ("token", "user", "application", "expires", "created_at")
    raw_id_fields = ("user", )

class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "user", "application")
    raw_id_fields = ("user", "access_token")

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(RefreshToken, RefreshTokenAdmin)
