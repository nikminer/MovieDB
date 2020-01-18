from django.contrib import admin
from Main.models import Serial, Season, Film, SeriesList, Genre, GenreF,GenreList

class FilmGenreInline(admin.TabularInline):
    model = GenreF

class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'originalname', 'year', 'length',  'rating')
    list_filter = ('year',)
    search_fields = ('name', 'originalname', 'disctiption',)
    inlines = [FilmGenreInline]

admin.site.register(Film,FilmAdmin)





class SeriesGenreInline(admin.TabularInline):
    model = Genre

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'originalname', 'episodelength', 'year', 'rating')
    list_filter = ('year',)
    search_fields = ('name', 'originalname')
    inlines = [SeriesGenreInline]

admin.site.register(Serial,SeriesAdmin)


class SeriesListInline(admin.TabularInline):
    model = SeriesList

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'status', 'episodecount', 'rating', )
    list_filter = ('status','serial', )
    search_fields = ('name', 'serial__name', 'disctiption', 'serial__originalname')
    raw_id_fields = ('serial',)
    inlines = [SeriesListInline]


admin.site.register(Season,SeasonAdmin)

class GenreListAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag')
    search_fields = ('name', 'tag')

admin.site.register(GenreList,GenreListAdmin)