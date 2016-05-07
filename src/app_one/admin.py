from app_one.models import *
from django.contrib import admin


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'description', 'created_timestamp')


class SnortieReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'message', 'status', 'created_timestamp')


class SnortieLimiterAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'message', 'status', 'created_timestamp')


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follow', 'created_timestamp')


admin.site.register(Image, ImageAdmin)
admin.site.register(SnortieLimiter, SnortieLimiterAdmin)
admin.site.register(SnortieReminder, SnortieReminderAdmin)
admin.site.register(UserFollow, UserFollowAdmin)
