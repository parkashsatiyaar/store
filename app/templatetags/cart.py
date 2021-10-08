from django import template

register = template.Library()

@register.filter(name='price_total')
def price_total(price, qn):
    price = price * qn
    return price