from django import template
from Order_App.models import Order

register = template.Library()

@register.filter
def cart_product_counter(user):
    order = Order.objects.filter(user=user,ordered=False)
    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0