from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ['title', 'content']

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)