from django.contrib import admin

from .models import (Statuses, Companies)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "phone_number")

class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "alias")


admin.site.register(Companies, CompanyAdmin)
admin.site.register(Statuses, StatusAdmin)

