from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(UserSet)
admin.site.register(Notification)
admin.site.register(HbA1c)
admin.site.register(medicalinformation)
admin.site.register(druginformation)
admin.site.register(set_default)
admin.site.register(Share)