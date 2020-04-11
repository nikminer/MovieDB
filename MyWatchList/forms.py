from django import forms
from .models import CommentModel

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Ваш комментарий","class":"text"}), label="", )
    spoiler = forms.BooleanField(required=False)

    class Meta:
        model = CommentModel
        fields = ('text', 'spoiler')