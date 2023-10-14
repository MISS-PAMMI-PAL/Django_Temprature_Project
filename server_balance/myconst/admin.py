from django.contrib import admin

from .models import MyState, UserNotifications, SlideContent
# Register your models here.

admin.site.register(MyState)
admin.site.register(UserNotifications)
admin.site.register(SlideContent)
