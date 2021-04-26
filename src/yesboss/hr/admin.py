from django.contrib import admin

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (Category, Schedules, Languages, Experience, Statuses, Resume, Vacancies)

class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "position_name", "created_dt")

class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class CategoryMPTTModelAdmin(MPTTModelAdmin):
    list_display = ("id", "name")
    mptt_level_indent = 20

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias")

class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias")

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias")

class VacancyAdmin(admin.ModelAdmin):
    list_display = ("id", "position_name", "created_dt")

admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Schedules, ScheduleAdmin)
admin.site.register(Languages, LanguageAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Statuses, StatusAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Vacancies, VacancyAdmin)
