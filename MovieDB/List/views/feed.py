from List.models import UserFeed
from Main.models import UserList,UserListF
from List.views.userstatus import UserStatusDict as UserStatus
from Profile.models import Profile

def rating(item): 
    return "Оцени{} {} на {} баллов".format(
        'ла' if Profile.objects.get(user=item.user).is_f else 'л',
        item.season.name if type(item) is UserList else '',
        item.userrate
    )

def status(item):
    return "Измени{} статус {} на {}".format(
        'ла' if Profile.objects.get(user=item.user).is_f else 'л',
        item.season.name if type(item) is UserList else '',
        UserStatus.get(item.userstatus)
    )

def inc(item):
    return "{}. Посмотре{} {} эпизод.".format(
        'ла' if Profile.objects.get(user=item.user).is_f else 'л',
        item.season.name if type(item) is UserList else '',
        item.userepisode
    )

typeFeed={
    "rating":{
        "type":"rating",
        "action": rating,
    },
    "status":{
        "type":"status",
        "action": status,
    },
    "inc":{
        "type":"inc",
        "action": inc,
    },
}

def sendFeed(item,typeFeedobj):
    if type(item) is UserList:
        UserFeed.objects.create(
            userlist=item,
            action=typeFeedobj['action'](item),
            typeAction=typeFeedobj['type'],
            user=Profile.objects.get(user=item.user)
        )
    elif type(item) is UserListF:
        UserFeed.objects.create(
            userlistF=item,
            action=typeFeedobj['action'](item),
            typeAction=typeFeedobj['type'],
            user=Profile.objects.get(user=item.user)
        )

def getFeed(feedlist):
    return UserFeed.objects.filter(user__in=feedlist).order_by("-created")[:60]