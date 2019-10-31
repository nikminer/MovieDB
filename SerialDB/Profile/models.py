
from django.db import models
from django.conf import settings
from datetime import datetime
from image_cropping import ImageRatioField

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users', default="users/default.png", blank=True)
    sex = models.CharField(max_length=1,choices=[('M','Муж'),('F','Жен')],default='1')
    photobg = models.ImageField(upload_to='users/bg',null=True, blank=True)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    @property
    def age(self):
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)


class Friendlist(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='link1')
    accepter = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='link2')
    status= models.IntegerField(default=0)


