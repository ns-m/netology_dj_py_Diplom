from django import template

register = template.Library()


@register.filter
def stars_rating(num: str) -> str:
    stars = ''
    if num:
        if num == 1:
            stars = '★'
        if num == 2:
            stars = '★★'
        if num == 3:
            stars = '★★★'
        if num == 4:
            stars = '★★★★'
        if num == 5:
            stars = '★★★★★'
    return stars
