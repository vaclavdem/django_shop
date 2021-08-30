from food.models import Users
from order.models import Cart, Order, Small_order

from .tasks import send_email

from django.db import models


def recalc_cart(cart):
    cart_data = cart.food.aggregate(models.Sum('final_price'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.save()


def logic(self, serializer):
    user = Users.objects.get(user=self.request.user)
    cart = Cart.objects.get(user=user)
    serializer.save(user=user, cart=cart, view_cart=cart.food.all(), final_price=cart.final_price)
    order = Order.objects.filter(user=user).last()
    order.small_order.clear()
    for food in cart.food.all():
        if food.restaurant in order.restaurants.all():
            pass
        else:
            order.restaurants.add(food.restaurant)
    for restaurant in order.restaurants.all():
        Small_order.objects.create(user=user, email=self.request.data.get("email"),
                                   name=self.request.data.get("name"), to=self.request.data.get("to"),
                                   comment=self.request.data.get("comment"), order=order,
                                   restaurant=restaurant, fromm=restaurant.address)
        small_order = Small_order.objects.filter(user=user).last()
        small_order.cart_product.set(cart.food.filter(restaurant=restaurant))
        order.small_order.add(small_order)
        data = small_order.cart_product.aggregate(models.Sum('final_price'))
        if data.get('final_price__sum'):
            small_order.final_price = data['final_price__sum']
        else:
            small_order.final_price = 0
        send_email("Заказ", "Из вашего ресторана создали заказ", restaurant.email)
        small_order.save()
    order.save()
    cart.food.clear()
    cart.final_price = 0
    cart.save()