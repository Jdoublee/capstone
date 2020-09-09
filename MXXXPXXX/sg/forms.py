from django import forms
from .models import User, Writing


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Writing
        fields = ['title', 'text', 'writer', 'category']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userid', 'password', 'name', 'email']
