from django.urls import path

import Serials.Seasons.views as views
import List.views.setseason as listsrc


 

urlpatterns = [
    path('<int:id>', views.season.season, name='season'),

    path('num/inc', views.numeric.incepisode, name="incepi"),
    path('num/set', views.numeric.setepisode, name="setepi"),
    path("num/dec", views.numeric.decepisode, name="decepi"),

    path('rewatch/inc', views.numeric.increwatched, name="increwtch"),
    path('rewatch/set', views.numeric.setrewatched, name="setrewtch"),
    path("rewatch/dec", views.numeric.decrewatched, name="decrewtch"),

    path("set/rating",listsrc.setrating,name="setrating"),
    path("set/status",listsrc.setstatus,name="setstatus"),
]

'''
    path("change/<int:id>",views.change.seasonch,name="seasonch"),
    path("change/<int:id>/name",views.change.seasonchname,name="seasonchname"),
    path("change/<int:id>/poster",views.change.seasonchposter,name="seasonchposter"),
    path("change/<int:id>/discription",views.change.seasonchdiscript,name="seasonchdiscript"),
    path("change/<int:id>/status",views.change.seasonchstatus,name="seasonchstatus"),
    path("change/<int:id>/episode/<int:epiid>",views.change.seasonchepisode,name="seasonchepisode"),
    path("change/<int:id>/episode/add",views.change.seasonchepisodeadd,name="seasonchepisodeadd"),
    path("change/<int:id>/episode/remove/<int:epiid>",views.change.seasonchepisoderm,name="seasonchepisoderm"),
    path("change/<int:id>/delete",views.change.seasonchdelete,name="seasonchdelete"),
'''

'''
urlpatterns = [
    
    path("addseasonpage",Season.addSeasonPage,name="addserialpage"),
    path("chseasonpage",Season.chSeasonPage,name="chseasonpage"),
    path("deleteseasonpage",Season.delSeasonPage,name="delseasonpage"),
]   
'''
