from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class StatusList(models.Model):
    name= models.TextField()
    color= models.TextField()

    def __str__(self):
        return self.name

class MovieManager(models.Manager):
    def get_series(self):
        return self.filter(series=True)

    def get_films(self):
        return self.filter(series=False)

    def get_seriesByUser(self, user):
        return self.get_series().filter(watchlist__user=user).distinct()

    def get_filmsByUser(self, user):
        return self.get_films().filter(watchlist__user=user)

class Movie(models.Model):
    name = models.TextField()
    originalname = models.TextField()

    length = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    kinopoiskid = models.PositiveIntegerField()
    disctiption = models.TextField(default="Нет данных")
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


class SeriesList(models.Model):
    season = models.ForeignKey(Season, related_name="serieslist", on_delete=models.CASCADE)
    name = models.TextField()
    date = models.DateField()

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
        from List.views.userstatus import UserStatusDict
        return UserStatusDict.get(self.userstatus)

    @property
    def get_statusTag(self):
        from List.views.userstatus import UserTagsStatusDict
        return UserTagsStatusDict.get(self.userstatus)


class CommentModel(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0)

    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    spoiler = models.BooleanField(default=False)
    active = models.BooleanField(default=True)