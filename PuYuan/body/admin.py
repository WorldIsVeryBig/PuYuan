from django.contrib import admin
from .models import *
# Register your models here.

class blood_pressure(admin.ModelAdmin):
    list_display = ['id', 'uid', 'systolic', 'diastolic', 'pulse', 'created_at', 'recorded_at', 'date']
class weight(admin.ModelAdmin):
    list_display = ['id', 'uid', 'weight', 'body_fat', 'bmi', 'created_at', 'recorded_at', 'date']

class blood_sugar(admin.ModelAdmin):
    list_display = ['id', 'uid', 'sugar', 'timeperiod', 'created_at', 'recorded_at', 'date']

class diary_diet(admin.ModelAdmin):
    list_display = ['id', 'uid', 'description', 'meal', 'tag', 'image_count', 'lat', 'lng', 'created_at', 'recorded_at', 'date']

class usercare(admin.ModelAdmin):
    list_display = ['id', 'uid', 'member_id', 'reply_id', 'message', 'created_at', 'updated_at', 'date']

admin.site.register(Blood_pressure, blood_pressure)
admin.site.register(Weight, weight)
admin.site.register(Blood_sugar, blood_sugar)
admin.site.register(Diary_diet, diary_diet)
admin.site.register(UserCare, usercare)