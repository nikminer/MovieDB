from django.contrib import admin
from .models import Movie, CommentModel, Season, SeriesList


class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'originalname', 'year', 'length', 'rating', 'release_date', 'series')
    list_filter = ('series','year', 'tags')
    search_fields = ('name', 'originalname', 'disctiption',)


admin.site.register(Movie, MovieAdmin)


class SeriesListInline(admin.TabularInline):
    model = SeriesList

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie', 'status', 'episodecount', 'rating',)
    list_filter = ('status', 'movie__tags', 'movie')
    search_fields = ('name', 'movie__name', 'disctiption', 'movie__originalname')
    raw_id_fields = ('movie',)
    inlines = [SeriesListInline]


admin.site.register(Season, SeasonAdmin)



class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'item', 'created','spoiler','active')
    list_filter = ('created',)

admin.site.register(CommentModel,ActionAdmin)
