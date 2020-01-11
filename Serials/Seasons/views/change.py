from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from Main.models import UserList,Season,Genre,Serial,StatusList,SeriesList
from django.contrib.auth.decorators import login_required,permission_required


from . import changeforms

import os
import re

UserStat={
    "planned":1,
    "watch":2,
    "watched":3,
    "rewatch":4,
    "drop":5
}


@login_required
def seasonch(request,id):
    data={
        "season":get_object_or_404(Season,id=id),
        "episodes":SeriesList.objects.filter(season_id=id).order_by('date')
    }
    return render(request,"Serials/season/seasonch.html",data)


@login_required
def seasonchname(request,id):
    season=get_object_or_404(Season,id=id)
    if request.method == 'POST':
        form = changeforms.ChNameForm(request.POST)
        if form.is_valid():
            season.name= form.cleaned_data['name']
            season.save()
            return redirect('season',id)
    else:
        form = changeforms.ChNameForm()
        form.fields['name'].initial=season.name

    return render(request, 'Serials/season/change/name.html', {
        'form': form,
        "season":season,
    })

@login_required
def seasonchposter(request,id):
    season=get_object_or_404(Season,id=id)
    if request.method == 'POST':
        form = changeforms.ChPosterForm(request.POST,request.FILES)
        if form.is_valid():
            season.img=form.cleaned_data['img']
            season.save()
            return redirect('season',id)
    else:
        form = changeforms.ChPosterForm()

    return render(request, 'Serials/season/change/poster.html', {
        'form': form,
        "season":season,
    })

@login_required
def seasonchdiscript(request,id):
    season=get_object_or_404(Season,id=id)
    if request.method == 'POST':
        form = changeforms.ChDiscriptForm(request.POST)
        if form.is_valid():
            season.disctiption=form.cleaned_data['discript']
            season.save()
            return redirect('season',id)
    else:
        form = changeforms.ChDiscriptForm()
        form.fields['discript'].initial=season.disctiption

    return render(request, 'Serials/season/change/discription.html', {
        'form': form,
        "season":season,
    })

@login_required
def seasonchstatus(request,id):
    season=get_object_or_404(Season,id=id)
    if request.method == 'POST':
        form = changeforms.ChStatusForm(request.POST)
        if form.is_valid():
            season.status_id=form.cleaned_data['status']
            season.save()
            return redirect('season',id)
    else:
        form = changeforms.ChStatusForm()
        form.fields['status'].initial=season.status_id

    return render(request, 'Serials/season/change/status.html', {
        'form': form,
        "season":season,
    })

@login_required
def seasonchepisode(request,id,epiid):

    season=get_object_or_404(Season,id=id)
    episode=get_object_or_404(SeriesList,id=epiid)
    if request.method == 'POST':
        form = changeforms.ChEpisodeForm(request.POST)
        if form.is_valid():
            episode.date=form.cleaned_data['date']
            episode.name=form.cleaned_data['name']
            episode.save()
            return redirect('seasonch',id)
    else:
        form = changeforms.ChEpisodeForm()
        form.fields['name'].initial=episode.name
        form.fields['date'].initial=episode.date

    return render(request, 'Serials/season/change/episode.html', {
        'form': form,
        "season":season,
        'episode':episode
    })

@login_required
def seasonchepisodeadd(request,id):
    season=get_object_or_404(Season,id=id)
    if request.method == 'POST':
        form = changeforms.ChEpisodeForm(request.POST)
        if form.is_valid():
            episode=SeriesList.objects.create(name=form.cleaned_data['name'],date=form.cleaned_data['date'].date(),season_id=id)
            episode.save()
            season.episodecount=len(SeriesList.objects.filter(season_id=id))
            season.save()
            return redirect('seasonch',id)
    else:
        form = changeforms.ChEpisodeForm()
        form.fields['name'].initial=str(len(SeriesList.objects.filter(season_id=id))+1)+" серия"
        
    return render(request, 'Serials/season/change/episodeadd.html', {
        'form': form,
        "season":season,
    })

@login_required
def seasonchepisoderm(request,id,epiid):
    episode=get_object_or_404(SeriesList,id=epiid)
    episode.delete()
    season=get_object_or_404(Season,id=id)
    season.episodecount=len(SeriesList.objects.filter(season_id=id))
    season.save()
    return redirect('seasonch',id)

@login_required
def seasonchdelete(request,id):
    for i in UserList.objects.filter(season_id=id):
        i.delete()

    season=get_object_or_404(Season,id=id)
    Serialid=season.serial.id
    season.delete()
    return redirect('serial',Serialid)