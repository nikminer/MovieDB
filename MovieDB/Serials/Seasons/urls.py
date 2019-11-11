from django.urls import path
from django.conf.urls import include

import Serials.Seasons.src as src
import List.views.setseason as listsrc
from django.conf import settings
from django.conf.urls.static import static


 

urlpatterns = [
    path('<int:id>',src.season.season,name='season'),

    path('num/inc',src.numeric.incepisode,name="incepi"),
    path('num/set',src.numeric.setepisode,name="setepi"),
    path("num/dec",src.numeric.decepisode,name="decepi"),

    path("set/rating",listsrc.setrating,name="setrating"),
    path("set/status",listsrc.setstatus,name="setstatus"),
]

'''
    path("change/<int:id>",src.change.seasonch,name="seasonch"),
    path("change/<int:id>/name",src.change.seasonchname,name="seasonchname"),
    path("change/<int:id>/poster",src.change.seasonchposter,name="seasonchposter"),
    path("change/<int:id>/discription",src.change.seasonchdiscript,name="seasonchdiscript"),
    path("change/<int:id>/status",src.change.seasonchstatus,name="seasonchstatus"),
    path("change/<int:id>/episode/<int:epiid>",src.change.seasonchepisode,name="seasonchepisode"),
    path("change/<int:id>/episode/add",src.change.seasonchepisodeadd,name="seasonchepisodeadd"),
    path("change/<int:id>/episode/remove/<int:epiid>",src.change.seasonchepisoderm,name="seasonchepisoderm"),
    path("change/<int:id>/delete",src.change.seasonchdelete,name="seasonchdelete"),
'''

'''
urlpatterns = [
    
    path("addseasonpage",Season.addSeasonPage,name="addserialpage"),
    path("chseasonpage",Season.chSeasonPage,name="chseasonpage"),
    path("deleteseasonpage",Season.delSeasonPage,name="delseasonpage"),
]   
'''
