from django.contrib import admin
from MyWatchList.models import CommentModel
from MyWatchList.models import Movie, Season, SeriesList
from MyWatchList.models import Notifications, Feed, Profile


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'originalname', 'year', 'length', 'rating', 'release_date', 'series')
    list_filter = ('series','year', 'tags')
    search_fields = ('name', 'originalname', 'disctiption',)

class SeriesListInline(admin.TabularInline):
    model = SeriesList

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie', 'status', 'episodecount', 'rating',)
    list_filter = ('status', 'movie__tags', 'movie')
    search_fields = ('name', 'movie__name', 'disctiption', 'movie__originalname')
    raw_id_fields = ('movie',)
    inlines = [SeriesListInline]

@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'item', 'created','spoiler','active')
    list_filter = ('created',)


@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'message', 'item', 'sended')
    list_filter = ('sended',)
    search_fields = ('message',)


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verb', 'item', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name','user', 'sex','age','date_of_birth')
    list_filter = ('sex',)
    search_fields = ('name','user')