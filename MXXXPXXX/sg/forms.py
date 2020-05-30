from django import forms
from .models import User


class ArticleTitle(forms.Form):
    article_title = forms.CharField()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userid','password', 'name', 'email']