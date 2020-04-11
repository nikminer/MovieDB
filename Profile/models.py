from django.db import models
from django.conf import settings
from datetime import datetime
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.auth.models import User


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
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)

    @property
    def countNoties(self):
        return Notifications.objects.filter(profile__user=self.user).count()

    @property
    def img(self):
        return self.photo

    def get_absolute_url(self):
        return "/profile/%s/" % self.user.username





class FriendsManager(models.Manager):
    def get_friends(self, profile):
        friends = []
        for i in self.filter(Q(accepter=profile) | Q(sender=profile)).filter(status=1):
            friends.append(i.getnotMyprofile(profile).user)
        return friends


class Friendlist(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='link1')
    accepter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='link2')
    status = models.IntegerField(default=0)
    friends = FriendsManager()
    objects = models.Manager()

    def getnotMyprofile(self, myprofile):
        if self.sender != myprofile and self.accepter == myprofile:
            return self.sender
        elif self.accepter != myprofile and self.sender == myprofile:
            return self.accepter
        else:
            return None


class Notifications(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    sended = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    item_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='item_notifi',
                                on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    item = GenericForeignKey('item_ct', 'item_id')


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