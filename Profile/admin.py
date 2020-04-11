from django.contrib import admin

from .models import Notifications,Feed, Profile
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

@admin.register(Profile)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name','user', 'sex','age','date_of_birth')
    list_filter = ('sex',)
    search_fields = ('name','user')