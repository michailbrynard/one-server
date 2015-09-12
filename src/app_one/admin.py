from app_one.models import *
from django.contrib import admin


class OneImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'description')


class OneGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'group_name', 'group_icon', 'status',
                    'created_timestamp', 'updated_timestamp')


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'status', 'created_timestamp', 'updated_timestamp')


class GroupImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_group', 'image', 'status', 'created_timestamp', 'updated_timestamp')


class SnortieReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'message', 'status', 'created_timestamp')


class SnortieLimiterAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'message', 'status', 'created_timestamp')


admin.site.register(OneImage, OneImageAdmin)
admin.site.register(OneGroup, OneGroupAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(GroupImage, GroupImageAdmin)
admin.site.register(SnortieLimiter, SnortieLimiterAdmin)
admin.site.register(SnortieReminder, SnortieReminderAdmin)
