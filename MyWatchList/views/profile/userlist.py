from MyWatchList.models import Profile
from django.forms import inlineformset_factory
from MyWatchList.models import Profile, UserList, UserListRecord
from django.shortcuts import render, get_object_or_404


def userList(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    userLists = UserList.objects.filter(user__username=username)
    '''
    UserListFormSet = inlineformset_factory(
      UserList,
      UserListRecord,
      fields = ('movie',),
      extra=1,

    )
    formset = UserListFormSet()
    data = {
        "formset": formset,
    }
    '''

    data = {
      'userlists': userLists,
      'profile':profile
    }
    return render(request, 'Profile/userlist.html', data)

