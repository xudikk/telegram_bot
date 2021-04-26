from django.contrib import admin

from .models import Users, Channel

class UserAdmin(admin.ModelAdmin):
    search_fields = ['user_id', 'username', 'phone_number']
    list_display = ("user_id", "user_id", "username",  "phone_number",  "created_at")

    readonly_fields = ['user_id']
    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    # def has_delete_permission(self, request, obj=None):
    #     return False

class ChannelAdmin(admin.ModelAdmin):
    list_display = ['username', 'token', 'vacancy_channel_link', 'resume_channel_link']


admin.site.register(Users, UserAdmin)
admin.site.register(Channel, ChannelAdmin)
