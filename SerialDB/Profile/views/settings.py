from django.shortcuts import render,redirect
from Profile.forms import UserProfileSettings
from Profile.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def Setbackground(request):
    from django.core.files.base import ContentFile
    import base64
    
    profile=Profile.objects.get(user=request.user)
    avatar=request.POST['Photo'].split(';base64,', 1 )
    ext = avatar[0].split('/')[-1]
    profile.photobg=ContentFile(base64.b64decode(avatar[1]), name=profile.user.username+'.' + ext)
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
    ext = avatar[0].split('/')[-1]
    profile.photo=ContentFile(base64.b64decode(avatar[1]), name=profile.user.username+'.' + ext)
    profile.save()

    from PIL import Image

    template=Image.open('./static/images/template.png').convert("RGBA")
    template.paste(Image.open(profile.photo.path).convert("RGBA"),Image.open('./static/images/mask.png').convert("RGBA"))
    template.save(profile.photo.path)

    messages.success(request, 'Аватар установлен успешно')

    return redirect('settings')

@login_required
def Prosettings(request):
    if request.method == 'POST':
        form = UserProfileSettings(request.POST)
        if form.is_valid():
            profile=Profile.objects.get(user=request.user)
            profile.user.first_name=form.cleaned_data['first_name']
            profile.user.last_name=form.cleaned_data['last_name']
            profile.date_of_birth=form.cleaned_data['date_of_birth']
            profile.user.save()
            profile.save()
            
            messages.success(request, 'Данные пользователя именены успешно')

            return redirect('profile',request.user.username)
    else:
        profile=Profile.objects.get(user=request.user)
        form=UserProfileSettings()
        form.initial['first_name']=profile.user.first_name
        form.fields['first_name'].required=True
        form.initial['last_name']=profile.user.last_name
        form.fields['last_name'].required=True
        form.initial['date_of_birth']=profile.date_of_birth
        data={
            "profile":profile,
            "settings":form
        }
        return render(request, 'Profile/settings.html',data)
