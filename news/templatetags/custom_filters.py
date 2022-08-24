from django import template
import re

register = template.Library()

BAD_WORDS = ['редиска', 'статьи']


@register.filter()
def censor(text):
    for word in BAD_WORDS:
        pattern = re.compile(word, re.IGNORECASE)
        text = re.sub(pattern, '*'*len(word), text, re.IGNORECASE)
    return text
