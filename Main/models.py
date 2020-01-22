from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse


class StatusList(models.Model):
    name= models.TextField()
    color= models.TextField()

    def __str__(self):
        return self.name

class Film(models.Model):
    name= models.TextField()
    originalname= models.TextField()
    status=models.ForeignKey(StatusList,default=1,on_delete=models.SET_DEFAULT)
    length= models.IntegerField()
    year=models.IntegerField()
    kinopoiskid= models.IntegerField()
    img= models.ImageField(upload_to='Posters', default="default.png")
    rating= models.FloatField(default=0,editable=False)
    disctiption= models.TextField(default="Нет данных")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return "/film/%i" % self.id
    
    @property
    def genre(self):
        return GenreF.objects.filter(film_id=self.id)

class Serial(models.Model):
    name= models.TextField()
    originalname= models.TextField()
    episodelength= models.IntegerField()
    year=models.IntegerField()
    kinopoiskid= models.IntegerField()
    img= models.ImageField(upload_to='Posters', default="default.png")

    def get_absolute_url(self):
        return "/serial/%i" % self.id

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)

    @property
    def genre(self):
        return Genre.objects.filter(serial_id=self.id)
    
    @property
    def seasons(self):
        return Season.objects.filter(serial_id=self.id)

    @property
    def rating(self):
        rating=Season.objects.filter(serial_id=self.id).filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
        if not rating:
            rating=0.00
        return round(rating,2)
    
class Season(models.Model):
    name= models.TextField()
    status=models.ForeignKey(StatusList,default=1,on_delete=models.SET_DEFAULT)
    episodecount= models.IntegerField()
    serial= models.ForeignKey(Serial,on_delete=models.CASCADE)
    disctiption= models.TextField(default="Нет данных")
    img= models.ImageField(upload_to='Posters', default="default.png")
    rating= models.FloatField(default=0,editable=False)

    class Meta:
        ordering = ('serial__name','name')
    def __str__(self):
        return str(self.name +" "+self.serial.name)

class SeriesList(models.Model):
    season= models.ForeignKey(Season,on_delete=models.CASCADE)
    name= models.TextField()
    date=models.DateField()

class GenreList(models.Model):
    name= models.TextField()
    tag= models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Genre(models.Model):
    genre= models.ForeignKey(GenreList,on_delete=models.CASCADE)
    serial= models.ForeignKey(Serial,on_delete=models.CASCADE)

class GenreF(models.Model):
    genre= models.ForeignKey(GenreList,on_delete=models.CASCADE)
    film= models.ForeignKey(Film,on_delete=models.CASCADE)

class UserList(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    season= models.ForeignKey(Season,on_delete=models.CASCADE)
    serial= models.ForeignKey(Serial,on_delete=models.CASCADE)
    userrate= models.IntegerField(default=0)
    userstatus= models.IntegerField(default=1)
    userepisode= models.IntegerField(default=0)
    countreview= models.IntegerField(default=0)
    
    @property
    def obj(self):
        return self.serial
    @property
    def get_absolute_url(self):
        return reverse("serial", kwargs={"id": self.serial.id})

    @property
    def get_status(self):
        from List.views.userstatus import UserStatusDict
        return UserStatusDict.get(self.userstatus)

    @property
    def get_statusTag(self):
        from List.views.userstatus import UserTagsStatusDict
        return UserTagsStatusDict.get(self.userstatus)

class UserListF(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    film= models.ForeignKey(Film,on_delete=models.CASCADE)
    userrate= models.IntegerField(default=0)
    userstatus= models.IntegerField(default=1)
    countreview= models.IntegerField(default=0)

    @property
    def obj(self):
        return self.film
    @property
    def get_absolute_url(self):
        return reverse("film", kwargs={"id": self.film.id})

    @property
    def get_status(self):
        from List.views.userstatus import UserStatusDict
        return UserStatusDict.get(self.userstatus)

    @property
    def get_statusTag(self):
        from List.views.userstatus import UserTagsStatusDict
        return UserTagsStatusDict.get(self.userstatus)