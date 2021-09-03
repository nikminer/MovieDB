import datetime
from django import forms
from django.contrib.auth.models import User


class UserProfileSettings(forms.ModelForm):
    date_of_birth = forms.DateTimeField(label='Дата рождения:', required=True,input_formats=['%Y-%m-%d'],widget= forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')),initial=datetime.date.today())
    class Meta:
        model = User
        fields = ('first_name','last_name')

class UserChangePass(forms.Form):
    oldpassword= forms.CharField(label='Старый пароль:', widget=forms.PasswordInput)
    password = forms.CharField(label='Новый пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput)

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return self.cleaned_data['password2']

