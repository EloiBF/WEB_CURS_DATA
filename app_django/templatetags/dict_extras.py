from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_index(lst, index):
    try:
        return lst[index]
    except (IndexError, TypeError):
        return None

@register.filter
def to_range(value):
    try:
        return range(int(value))
    except:
        return []

@register.filter
def dict_first_key(d):
    """Retorna la primera clau d’un diccionari (per a saber quants elements té una columna)"""
    return next(iter(d), None)

@register.filter
def to_chr(value):
    try:
        return chr(int(value))
    except (ValueError, TypeError):
        return ''
