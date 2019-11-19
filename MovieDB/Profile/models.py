
from django.db import models
from django.conf import settings
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users', default="users/default.png", blank=True)
    sex = models.CharField(max_length=1,choices=[('M','Муж'),('F','Жен')],default='1')
    photobg = models.ImageField(upload_to='users/bg',null=True, blank=True)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    @property
    def is_f(self):
        return self.sex=="F"
        
    @property
    def age(self):
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)

    def get_absolute_url(self):
        return "/profile/%s/" % self.user.username


class Friendlist(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='link1')
    accepter = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='link2')
    status= models.IntegerField(default=0)

    def getnotMyprofile(self,myprofile):
        if self.sender != myprofile and self.accepter==myprofile: 
            return self.sender
        elif self.accepter != myprofile and self.sender == myprofile:
            return self.accepter
        else:
            return None
