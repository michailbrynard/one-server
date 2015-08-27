from app_one.models import *
from django.contrib import admin


class OneImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'description')


class OneGroupAdmin(admin.ModelAdmin):
    list_display = ('creator', 'group_name', 'group_icon', 'status',
                    'created_timestamp', 'updated_timestamp')


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'status', 'created_timestamp', 'updated_timestamp')


class GroupImageAdmin(admin.ModelAdmin):
    list_display = ('user_group', 'image', 'status', 'created_timestamp', 'updated_timestamp')


admin.site.register(OneImage, OneImageAdmin)
admin.site.register(OneGroup, OneGroupAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(GroupImage, GroupImageAdmin)

