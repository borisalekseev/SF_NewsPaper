from allauth.socialaccount.forms import SignupForm as SocSignupForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from django.core.exceptions import ValidationError

from .models import Post, User, Author


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user


class SocialSignupForm(SocSignupForm):

    def save(self, request):
        user = super(SocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'category', 'text']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
