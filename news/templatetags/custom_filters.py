from django import template
import re
from ..models import TYPE_CHOICES

register = template.Library()

BAD_WORDS = ['редиска', 'статьи']
MANY = {'Статья': 'Статьи', 'Новость': 'Новости'}


@register.filter()
def censor(text):
    for word in BAD_WORDS:
        pattern = re.compile(word, re.IGNORECASE)
        text = re.sub(pattern, '*'*len(word), text, re.IGNORECASE)
    return text


@register.filter()
def ru_type(text): return dict(TYPE_CHOICES)[text]


"""Only for main articles and news pages filter"""
@register.filter()
def get_category(post_objects): return MANY[post_objects[0].type]
