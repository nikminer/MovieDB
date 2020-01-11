from django.urls import path
from django.conf.urls import url
from Profile import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('logout-then-login/',views.auth.logoutthenlogin, name='logout'),
    path('register/',views.auth.register, name='register'),

    path('settings/',views.settings.Prosettings ,name="settings"),
    path('settings/avatar',views.settings.Setavatar ,name="setavatar"),
    path('settings/bg',views.settings.Setbackground,name="setbackground"),
    path('settings/resetbg',views.settings.ResetBG,name="resetbackground"),

    path('<str:username>/',views.profile ,name="profile"),

    path('noties',views.notifications.notifications ,name="noties"),
    path('noties/del',views.notifications.deletenotification ,name="delnoties"),


    path('<str:username>/dialog',views.messages.Dialog ,name="dialog"),
    path('<str:username>/sendmessage',views.messages.SendMessage ,name="sendmessage"),

    path('<str:username>/friends',views.friends.Friends ,name="friends"),
    path('<str:username>/requests',views.friends.Friendsreq ,name="friendreq"),
    path('<str:username>/addfriend',views.friends.addfriend ,name="addfriend"),
    path('<str:username>/remfriend',views.friends.Removefriend ,name="remfriend"),
    path('<str:username>/accept/<int:id>',views.friends.Acceptfriend ,name="acceptfriend"),
    path('<str:username>/decline/<int:id>',views.friends.Declinefriend ,name="declinefriend"),

]
