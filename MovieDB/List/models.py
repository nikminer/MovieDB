from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from Main.models import UserList,UserListF
from datetime import datetime

class UserFeed(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    userlist=models.ForeignKey(UserList,on_delete=models.CASCADE,null=True)
    userlistF=models.ForeignKey(UserListF,on_delete=models.CASCADE,null=True)
    @property
    def list(self):
        if self.userlist:
            return self.userlist
        else:
            return self.userlistF

    @property
    def is_lasthour(self):
        from django.utils.timezone import make_aware
        return (make_aware(datetime.now())-self.created).seconds < 3600

    def save(self, *args, **kwargs):
        self.created=datetime.now()
        super(UserFeed, self).save(*args, **kwargs)

    created = models.DateTimeField(auto_now_add=True)

    action = models.TextField()
    lastaction = models.TextField(blank=True)
    typeAction = models.TextField(null=True)