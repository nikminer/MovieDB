from MyWatchList.views.profile import userlist
from django.urls import path
from MyWatchList.views import profile as views


from django.contrib.auth import views as Authviews

urlpatterns = [
    path('logout/', views.auth.logoutthenlogin, name='logout'),
    path('login/', views.auth.loginView, name='login'),

    path('password_reset/',
         Authviews.PasswordResetView.as_view(
             template_name="Profile/auth/reset.html",
             email_template_name="Profile/auth/password_reset_form.html"),
         name='password_reset'),

    path('password_reset/done/',
         Authviews.PasswordResetDoneView.as_view(
             template_name="Profile/auth/password_reset_done.html", ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         Authviews.PasswordResetConfirmView.as_view(
             template_name="Profile/auth/password_reset_confirm.html"
         ),
         name='password_reset_confirm'),
    path('reset/done/', views.auth.resetpasswordDone, name='password_reset_complete'),

    path('register/', views.auth.register, name='register'),

    path('settings/', views.settings.Prosettings, name="settings"),
    path('settings/avatar', views.settings.Setavatar, name="setavatar"),
    path('settings/bg', views.settings.Setbackground, name="setbackground"),
    path('settings/resetbg', views.settings.ResetBG, name="resetbackground"),

    path('<str:username>/', views.profile, name="profile"),

    path('noties', views.notifications.notifications, name="noties"),
    path('noties/del', views.notifications.deletenotification, name="delnoties"),

    path('<str:username>/dialog', views.messages.Dialog, name="dialog"),
    path('<str:username>/sendmessage', views.messages.SendMessage, name="sendmessage"),


    path('<str:username>/activity/<int:page>', views.feed.Profileactivity, name='ProfileActivity_page'),
    path('<str:username>/index/<int:page>', views.feed.Indexactivity, name='IndexActivity_page'),

    path('<str:username>/followers', views.followers.followers, name="followers"),
    path('<str:username>/followings', views.followers.following, name="followings"),
    path('<str:username>/follow', views.followers.follow, name="follow"),
    path('<str:username>/userlist', views.userlist.userList),
]
