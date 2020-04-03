from django.contrib import admin

from .models import Notifications,Feed
@admin.register(Notifications)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'message', 'item', 'sended')
    list_filter = ('sended',)
    search_fields = ('message',)


@admin.register(Feed)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verb', 'item', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)