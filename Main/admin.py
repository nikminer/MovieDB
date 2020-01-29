from django.contrib import admin
from Main.models import Serial, Season, Film, SeriesList



class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'originalname', 'year', 'length',  'rating')
    list_filter = ('year','tags')
    search_fields = ('name', 'originalname', 'disctiption',)

admin.site.register(Film,FilmAdmin)




class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'originalname', 'episodelength', 'year', 'rating',)
    list_filter = ('year','tags')
    search_fields = ('name', 'originalname')


admin.site.register(Serial,SeriesAdmin)


class SeriesListInline(admin.TabularInline):
    model = SeriesList

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'status', 'episodecount', 'rating', )
    list_filter = ('status','serial__tags','serial' )
    search_fields = ('name', 'serial__name', 'disctiption', 'serial__originalname')
    raw_id_fields = ('serial',)
    inlines = [SeriesListInline]


admin.site.register(Season,SeasonAdmin)

from django.contrib import admin
from .models import Comment
@admin.register(Comment)
class ActionAdmin(admin.ModelAdmin):
 list_display = ('user', 'text', 'item', 'created','spoiler','active')
 list_filter = ('created',)