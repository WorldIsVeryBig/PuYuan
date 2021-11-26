from django.contrib import admin
from .models import *
# Register your models here.

class friend(admin.ModelAdmin):
    list_display = ['id', 'uid', 'invite_code', 'created_at', 'date']

class friend_data(admin.ModelAdmin):
    list_display = ['id', 'uid', 'relation_id', 'friend_type', 'status', 'read', 'imread', 'created_at', 'updated_at', 'date']

admin.site.register(Friend, friend)
admin.site.register(Friend_data, friend_data)