from django import forms
from django.core.exceptions import ValidationError

from .models import Post, TYPE_CHOICES


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'category', 'text']
