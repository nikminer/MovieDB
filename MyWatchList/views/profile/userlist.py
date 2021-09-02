from django.forms import inlineformset_factory
from MyWatchList.models import UserList, UserListRecord


def userList(request, username):
    profile = get_object_or_404(Profile, user__username=username)


    UserListFormSet = inlineformset_factory(
      UserList,
      UserListRecord,
      fields = ('movie'),
      extra=1,
    )
    formset = UserListFormSet()
    data = {
        "formset": formset,
    }
    return render(request, 'Profile/profile.html', data)

