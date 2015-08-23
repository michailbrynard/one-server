from django.contrib import admin

# Register your models here.
from app_one.models import *


admin.site.register(OneImage)
admin.site.register(OneGroup)
admin.site.register(UserGroup)
admin.site.register(GroupImage)

