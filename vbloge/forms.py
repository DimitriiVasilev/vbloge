from django.forms import ModelForm, PasswordInput
from .models import Category, Article, Profile, Comment
from django.contrib.auth.models import User


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': PasswordInput()
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', ]


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
