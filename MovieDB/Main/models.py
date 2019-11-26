from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse

class StatusList(models.Model):
    name= models.TextField()
    color= models.TextField()

class Movie(models.Model):
    kinopoiskid= models.IntegerField()

    name= models.TextField()
    originalname= models.TextField()
    
    year=models.IntegerField()

    status=models.ForeignKey(StatusList,default=1,on_delete=models.SET_DEFAULT)
    
    length= models.IntegerField()

    disctiption= models.TextField(default="Нет данных")

    @property
    def genre(self):
        return Genre.objects.filter(movie_id=self.id)

class Posters(models.Model):
    img= models.ImageField(upload_to='Posters')
    movie= models.ForeignKey(Movie,default=1,on_delete=models.SET_DEFAULT,null=True)

class Film(models.Model):
    movie= models.ForeignKey(Movie,default=1,on_delete=models.SET_DEFAULT)

    rating= models.FloatField(default=0)

    poster= models.ForeignKey(Posters,default=1,on_delete=models.SET_DEFAULT)

    def get_absolute_url(self):
        return "/film/%i" % self.id
        

class Series(models.Model):
    movie=models.ForeignKey(Movie,default=1,on_delete=models.SET_DEFAULT)

    poster= models.ForeignKey(Posters,default=1,on_delete=models.SET_DEFAULT)

    @property
    def rating(self):
        rating=self.seasons.filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
        if not rating:
            rating=0.00
        return round(rating,2)

    def get_absolute_url(self):
        return "/serial/%i" % self.id

    @property
    def seasons(self):
        return Season.objects.filter(series_id=self.id).order_by("name")

class Season(models.Model):
    
    series= models.ForeignKey(Series,on_delete=models.CASCADE,default=1)

    name= models.TextField()

    status=models.ForeignKey(StatusList,default=1,on_delete=models.SET_DEFAULT)

    episodecount= models.IntegerField()
    
    disctiption= models.TextField(default="Нет данных")

    poster= models.ForeignKey(Posters,default=1,on_delete=models.SET_DEFAULT)

    rating= models.FloatField(default=0)


class SeriesList(models.Model):
    season= models.ForeignKey(Season,on_delete=models.CASCADE)
    name= models.TextField()
    date=models.DateField()


class GenreList(models.Model):
    name= models.TextField()
    tag= models.TextField()

class Genre(models.Model):
    genre= models.ForeignKey(GenreList,on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE,default=1)



class UserListF(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE,default=1)
    
    userrate= models.IntegerField(default=0)
    userstatus= models.IntegerField(default=1)
    countreview= models.IntegerField(default=0)

    @property
    def get_absolute_url(self):
        return reverse("film", kwargs={"id": self.movie.id})

class UserListS(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE,default=1)
    season= models.ForeignKey(Season,on_delete=models.CASCADE)

    userrate= models.IntegerField(default=0)
    userstatus= models.IntegerField(default=1)
    countreview= models.IntegerField(default=0)

    userepisode= models.IntegerField(default=0)

    @property
    def get_absolute_url(self):
        return reverse("serial", kwargs={"id": self.movie.id})

