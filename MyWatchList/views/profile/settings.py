from django.shortcuts import render,redirect
from MyWatchList.forms.Settings import UserProfileSettings,UserChangePass
from MyWatchList.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MovieNet.settings import STATICFILES_DIRS
from django.contrib.auth import authenticate,login



@login_required
def Setbackground(request):
    from django.core.files.base import ContentFile
    import base64
    
    profile=Profile.objects.get(user=request.user)
    avatar=request.POST['Photo'].split(';base64,', 1)

    profile.photobg=ContentFile(base64.b64decode(avatar[1]), name=str(profile.user.id)+'.' + avatar[0].split('/')[-1])
    profile.save()
    messages.success(request, 'Задний фон установлен успешно')

    return redirect('settings')

@login_required
def ResetBG(request):
    profile=Profile.objects.get(user=request.user)
    profile.photobg=None
    profile.save()
    messages.success(request, 'Задний фон сброшен успешно')
    return redirect('settings')

@login_required
def Setavatar(request):
    from django.core.files.base import ContentFile
    import base64
    profile=Profile.objects.get(user=request.user)
    avatar=request.POST['Photo'].split(';base64,', 1 )

    profile.photo=ContentFile(base64.b64decode(avatar[1]), name=str(profile.user.id)+'.' + avatar[0].split('/')[-1])
    profile.save()

    from PIL import Image
    import os
    template=Image.open( os.path.join(STATICFILES_DIRS[0],'images','template.png')).convert("RGBA")
    template.paste(Image.open(profile.photo.path).convert("RGBA"),Image.open(os.path.join(STATICFILES_DIRS[0],'images','mask.png')).convert("RGBA"))
    template.save(profile.photo.path)

    messages.success(request, 'Аватар установлен успешно')

    return redirect('settings')



@login_required
def Prosettings(request):

    profile = request.user.profile

    data ={
        "profile": profile
    }



    if request.method == 'POST' and request.POST['type'] == 'userinfo':
        form = UserProfileSettings(request.POST)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.user.save()
            profile.save()

            messages.success(request, 'Данные пользователя именены успешно')
        else:
            data.update({"settings": form})
    else:
        form = UserProfileSettings()
        form.initial['first_name'] = profile.user.first_name
        form.fields['first_name'].required = True
        form.initial['last_name'] = profile.user.last_name
        form.fields['last_name'].required = True
        form.initial['date_of_birth'] = profile.date_of_birth
        data.update({"settings": form})



    if request.method == 'POST' and request.POST['type'] == 'chpass':
        form = UserChangePass(request.POST)
        if form.is_valid():
            user= authenticate(username=request.user.username, password=form.cleaned_data['oldpassword'])
            if user:
                user.set_password(form.cleaned_data['password2'])
                user.save()

                login(request, user)
                messages.success(request, 'Данные пользователя именены успешно')
                data.update({"chengePass":  UserChangePass()})
            else:
                form.add_error('oldpassword', "Неверный пароль")
                data.update({"chengePass": form})
        else:
            data.update({"chengePass": form})
    else:
        form = UserChangePass()
        data.update({"chengePass": form})


    return render(request, 'Profile/settings.html', data)