from django import forms
import datetime
class ChNameForm (forms.Form):
    name= forms.CharField(label='Имя сезона')

class ChPosterForm (forms.Form):
    img= forms.ImageField(label='Загрузка нового постера',widget=forms.FileInput(attrs={'onchange':'getImage(this)'}))

class ChDiscriptForm (forms.Form):
    discript=forms.CharField(label='Описание сезона',widget=forms.Textarea(attrs={'placeholder': "Описание", 'rows': 12}),required=False)
    
class ChStatusForm (forms.Form):
    status=forms.ChoiceField(label='Статус сезона',choices=((1, "Анонс"), (2, "Идёт"), (3, "Вышел")))

class ChEpisodeForm (forms.Form):
    name= forms.CharField(label='Название эпизода')
    date= forms.DateTimeField(label='Дата выхода',input_formats=['%Y-%m-%d'],widget= forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')),initial=datetime.date.today())