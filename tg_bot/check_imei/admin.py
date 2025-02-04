from django.contrib import admin

from .models import *

@admin.register(UserTgBot)
class PrivatePersonAdmin(admin.ModelAdmin):
    fields = ('name', 'username', 'user_id', 'access_is_allowed')
