from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class StatusList(models.Model):
    name= models.TextField()
    color= models.TextField()

    def __str__(self):
        return self.name

class MovieManager(models.Manager):
    def get_series(self):
        return self.filter(series=True, active=True)

    def get_films(self):
        return self.filter(series=False, active=True)

    def get_seriesByUser(self, user):
        return self.get_series().filter(watchlist__user=user, active=True).distinct()

    def get_filmsByUser(self, user):
        return self.get_films().filter(watchlist__user=user, active=True)

class Movie(models.Model):
    active = models.BooleanField(default=True)

    name = models.TextField()
    originalname = models.TextField()

    length = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField()

    release_date = models.DateField(default=datetime.date.today)
    release_dateRU = models.DateField(default=datetime.date.today)

    UScert = models.CharField(null=True, max_length=10, blank=True )
    RUcert = models.CharField(null=True, max_length=10, blank=True)

    tmdbid = models.CharField(max_length=100)
    imdbid = models.CharField(null=True, blank=True, max_length=100)
    kinopoiskid = models.PositiveIntegerField(null=True, blank=True)

    disctiption = models.TextField(null=True, blank=True)
    rating = models.FloatField(default=0, editable=False)

    tags = TaggableManager()

    series = models.BooleanField(default=False)

    img = models.ImageField(upload_to='Posters', default="default.png")

    manager = MovieManager()
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        if self.series:
            return reverse("serial", kwargs={"id": self.id})
        else:
            return reverse("film", kwargs={"id": self.id})

    def get_seasons(self):
        if self.series:
            return self.season.all()


class Season(models.Model):

    movie = models.ForeignKey(Movie, null=True, related_name="season", on_delete=models.CASCADE)
    status = models.ForeignKey(StatusList, default=1, on_delete=models.SET_DEFAULT)

    name = models.TextField()
    episodecount = models.IntegerField()
    position = models.PositiveSmallIntegerField(default=0)

    img = models.ImageField(upload_to='Posters', default="default.png")

    rating = models.FloatField(default=0, editable=False)

    tmdbid = models.CharField(max_length=100)

    disctiption = models.TextField(default="Нет данных")

    def get_date(self):
        result=None
        try:
            result= self.serieslist.all().order_by('date').first().date
        except:
            pass
        return result

    class Meta:
        ordering = ('movie__name', 'position', 'name')

    def __str__(self):
        return str(self.name + " " + self.movie.name)

    def get_absolute_url(self):
        return reverse("season", kwargs={"id": self.id})

class SeriesList(models.Model):
    season = models.ForeignKey(Season, related_name="serieslist", on_delete=models.CASCADE)
    name = models.TextField()
    date = models.DateField()
    disctiption = models.TextField(default="Нет данных", null=True, blank=True)

class WatchListManager(models.Manager):
    def get_series(self):
        return self.filter(movie__series=True)

    def get_seasons(self, wl):
        return self.filter(movie=wl.movie)

    def get_films(self):
        return self.filter(movie__series=False)


class WatchList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE)
    season= models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    userrate= models.PositiveSmallIntegerField(default=0)
    userstatus= models.PositiveSmallIntegerField(default=1)
    rewatch= models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    userepisode = models.PositiveIntegerField(default=0, null=True)

    manager = WatchListManager()
    objects = models.Manager()

    @property
    def get_status(self):
        from MyWatchList.views.list.userstatus import UserStatusDict
        return UserStatusDict.get(self.userstatus)

    @property
    def get_statusTag(self):
        from MyWatchList.views.list.userstatus import UserTagsStatusDict
        return UserTagsStatusDict.get(self.userstatus)

class CommentManager(models.Manager):
    def get_comments(self, item):
        return self.filter(content_type=ContentType.objects.get_for_model(item), object_id=item.id)

class CommentModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    comments = CommentManager()
    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0)

    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    spoiler = models.BooleanField(default=False)
    active = models.BooleanField(default=True)