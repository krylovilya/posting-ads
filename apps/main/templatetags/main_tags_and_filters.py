from random import randint

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def number_of_user_notifications() -> int:
    """Возвращает количество уведомлений у пользователя."""
    return randint(0, 10)


@register.filter
@stringfilter
def string_inversion(value: str) -> str:
    """Переворачивает строку"""
    return value[::-1]


@register.filter
@stringfilter
def save_tag_in_url(tag_name):
    if not tag_name:
        return ''
    return f'&tag={tag_name}'
