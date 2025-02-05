from django.contrib import admin

from .models import *

@admin.register(UserTgBot)
class PrivatePersonAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id',)
    fields = ('name', 'username', 'user_id', 'access_is_allowed')
    list_display = ('name', 'username', 'user_id', 'access_is_allowed')

