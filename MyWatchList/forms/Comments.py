from django import forms
from .models import CommentModel, ReplyModel

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Ваш комментарий","class":"text"}), label="", )
    spoiler = forms.BooleanField(required=False)

    class Meta:
        model = CommentModel
        fields = ('text', 'spoiler')

class ReplyForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Ваш ответ","class":"text", 'rows': 1,}), label="", )
    spoiler = forms.BooleanField(required=False)
    class Meta:
        model = ReplyModel
        fields = ('text', 'spoiler')