from List.models import UserFeed
from Main.models import UserListS,UserListF
from List.views.userstatus import UserStatusDict as UserStatus
from Profile.models import Profile
import re

def rating(item): 
    return "Оцени{} {} на {} баллов".format(
        'ла' if Profile.objects.get(user=item.user).is_f else 'л',
        item.season.name if type(item) is UserListS else '',
        item.userrate
    )

def status(item):
    return "Измени{} статус {} на {}".format(
        'ла' if Profile.objects.get(user=item.user).is_f else 'л',
        item.season.name if type(item) is UserListS else '',
        UserStatus.get(item.userstatus)
    )

def inc(item):
    return "{}. Посмотре{} {} эпизод.".format(
        item.season.name if type(item) is UserListS else '',
        'ла' if Profile.objects.get(user=item.user).is_f else 'л',
        item.userepisode
    )

def incchange(useritem):
    regular = re.search(r"по \d+ эпизод.", useritem.action)
    action= re.split(r"\d+ эпизод.",useritem.action)[0]
    if regular:
        action+= "{} эпизод.".format(
            useritem.list.userepisode+1
        )
    else:
        regular = re.search(r"\d+ эпизод.", useritem.action)
        action+= "c {} по {} эпизод.".format(
            re.split(" эпизод.",regular[0])[0],
            useritem.list.userepisode+1
        )
    return action 


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
        "change": incchange,
    },
}

def sendFeed(item,typeFeedobj):
    if type(item) is UserListS:
        itemfeed = UserFeed.objects.filter(userlistS=item,typeAction=typeFeedobj['type'], user=Profile.objects.get(user=item.user)).order_by('-created').first()
    elif type(item) is UserListF: 
        itemfeed = UserFeed.objects.filter(userlistF=item,typeAction=typeFeedobj['type'], user=Profile.objects.get(user=item.user)).order_by('-created').first()

    if itemfeed and itemfeed.is_lasthour and typeFeedobj.get('change'):
        itemfeed.action=typeFeedobj['change'](itemfeed)
        itemfeed.save()
    else:
        if type(item) is UserListS:
            UserFeed.objects.create(
                userlistS=item,
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