from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from Profile.forms import LoginForm,UserRegistrationForm
from Profile.models import Profile

def loginView(request):
    data={}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                data.update({'error': "Неверный логин или пароль"})
    else:
        form = LoginForm()

    data.update({'form': form})
    return render(request, 'Profile/auth/login.html',data)

def logoutthenlogin(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user,date_of_birth=user_form.cleaned_data['date_of_birth'],sex=user_form.cleaned_data['sex'])
            
            login(request, new_user)
            return redirect('index')
    else:
        user_form = UserRegistrationForm()
        user_form.fields['first_name'].required=True
        user_form.fields['last_name'].required=True
        user_form.fields['email'].required=True
    return render(request, 'Profile/auth/register.html', {'form': user_form})