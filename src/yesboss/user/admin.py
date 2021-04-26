from django.contrib import admin

from .models import (Types, Statuses, Users)


class TypesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number", "first_name", "date_joined")

admin.site.register(Types, TypesAdmin)
admin.site.register(Statuses, StatusAdmin)
admin.site.register(Users, UserAdmin)
