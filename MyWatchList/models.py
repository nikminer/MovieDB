from django.db import models
from taggit.managers import TaggableManager


class StatusList(models.Model):
    name= models.TextField()
    color= models.TextField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.TextField()
    originalname = models.TextField()

    length = models.IntegerField()
    year = models.IntegerField()
    kinopoiskid = models.PositiveIntegerField()

    tags = TaggableManager()

    img = models.ImageField(upload_to='Posters', default="default.png")


class Film(models.Model):
    movie = models.ForeignKey(Movie, null=True, related_name="film", on_delete=models.CASCADE)

    rating = models.FloatField(default=0, editable=False)

    disctiption = models.TextField(default="Нет данных")

    def __str__(self):
        return self.movie.name

    class Meta:
        ordering = ('movie__name',)

    def get_absolute_url(self):
        return "/film/details/%i" % self.id


class Serial(models.Model):
    movie = models.ForeignKey(Movie, null=True, related_name="serial", on_delete=models.CASCADE)

    rating = models.FloatField(default=0, editable=False)

    disctiption = models.TextField(default="Нет данных")

    def get_absolute_url(self):
        return "/serial/details/%i" % self.id

    def __str__(self):
        return self.movie.name

    class Meta:
        ordering = ('movie__name',)

    @property
    def seasons(self):
        return Season.objects.filter(serial_id=self.id)

    @property
    def rating(self):
        rating = Season.objects.filter(serial_id=self.id).filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
        if not rating:
            rating = 0.00
        return round(rating, 2)


class Season(models.Model):
    name = models.TextField()

    serial = models.ForeignKey(Serial, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusList, default=1, on_delete=models.SET_DEFAULT)

    episodecount = models.IntegerField()
    position = models.PositiveSmallIntegerField(default=0)

    img = models.ImageField(upload_to='Posters', default="default.png")

    rating = models.FloatField(default=0, editable=False)

    disctiption = models.TextField(default="Нет данных")

    class Meta:
        ordering = ('serial__movie__name', 'position', 'name')

    def __str__(self):
        return str(self.name + " " + self.serial.movie.name)


class SeriesList(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    name = models.TextField()
    date = models.DateField()
