import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from ..models import Feed


def create_feed(profile, verb, item=None):
    last_minute = timezone.now() - datetime.timedelta(seconds=60)
    similar_actions = Feed.objects.filter(profile=profile, verb=verb,
                                          created__gte=last_minute)
    if item:
        item_ct = ContentType.objects.get_for_model(item)
        similar_actions = similar_actions.filter(item_ct=item_ct,
                                                 item_id=item.id)
    if not similar_actions:
        action = Feed(profile=profile, verb=verb, item=item)
        action.save()
        return True
    return False

