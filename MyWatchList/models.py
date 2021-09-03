import datetime
from django.db import models
from taggit.managers import TaggableManager

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.urls import reverse


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


class StatusList(models.Model):
    name= models.TextField()
    color= models.TextField()

    def __str__(self):
        return self.name

class Season(models.Model):

    movie = models.ForeignKey(Movie, null=True, related_name="season", on_delete=models.CASCADE)
    status = models.ForeignKey(StatusList, default=1, on_delete=models.SET_DEFAULT)

    name = models.TextField()
    episodecount = models.IntegerField()
    position = models.PositiveSmallIntegerField(default=0)

    img = models.ImageField(upload_to='Posters', default="default.png")

    rating = models.FloatField(default=0, editable=False)

    tmdbid = models.CharField(max_length=100, null=True, blank=True)

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






class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users', default="users/default.png", blank=True)
    sex = models.CharField(max_length=1, choices=[('M', 'Муж'), ('F', 'Жен')], default='1')
    photobg = models.ImageField(upload_to='users/bg', null=True, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    @property
    def name(self):
        return " ".join((self.user.first_name, self.user.last_name))

    @property
    def is_f(self):
        return self.sex == "F"

    @property
    def age(self):
        from dateutil.relativedelta import relativedelta
        today = datetime.datetime.today()
        delta = relativedelta(today, self.date_of_birth)
        return delta.years

    @property
    def countNoties(self):
        return Notifications.objects.filter(profile__user=self.user).count()

    @property
    def img(self):
        return self.photo

    def get_absolute_url(self):
        return "/profile/%s/" % self.user.username


class MessageManager(models.Manager):
    def get_dialog(self, sender, accepter):
        return self.filter(Q(FromUser=accepter, ToUser=sender) | Q(FromUser=sender, ToUser=accepter)).order_by(
            "-sended")

class Messages(models.Model):
    FromUser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='From')
    ToUser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='To')

    sended = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    objects = MessageManager()



class Notifications(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    sended = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    item_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='item_notifi',
                                on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    item = GenericForeignKey('item_ct', 'item_id')



class Feed(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    item_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='item_obj',
                                on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('item_ct', 'item_id')

    created = models.DateTimeField(auto_now_add=True)

    feed_type = models.CharField(max_length=20, null=True)
    verb = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} {}'.format(self.profile, self.verb)



class Follower(models.Model):
    follow_from = models.ForeignKey(Profile, related_name='rel_from_set', on_delete=models.CASCADE)
    follow_to = models.ForeignKey(Profile, related_name='rel_to_set', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows to {}'.format(self.follow_from, self.follow_to)


Profile.add_to_class('following',
                     models.ManyToManyField('self', through=Follower, related_name='followers', symmetrical=False))



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

class UserList(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserListRecord(models.Model):
    header = models.ForeignKey(UserList, on_delete=models.CASCADE)
    movie  = models.ForeignKey(Movie, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('header', 'movie')