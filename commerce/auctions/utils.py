from django.template.defaultfilters import slugify
from random import choice
from string import ascii_letters
from re import search
from .models import Listing

"""
handle cyrillic letters
"""


def check_cyrillic(title):
    return bool(search('[а-яА-Я]', title))


def translate_cyrillic(title):
    translated_title = title.translate(
        str.maketrans(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
    return translated_title


"""
Slug generation
"""


def create_unique_slug(title):
    new_slug = slugify(title)
    check_slug = Listing.objects.filter(slug=new_slug)
    if check_slug.exists():
        new_slug = f"{new_slug}_{choice(ascii_letters)}{choice(ascii_letters)}" \
                   f"{choice(ascii_letters)}{choice(ascii_letters)}"
    return new_slug
