from django import template

register = template.Library()


@register.filter
def order_total(order):
    return sum(item.product.price * item.quantity for item in order.items.all())