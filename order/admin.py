from django.contrib import admin

from .models import (
    Status,
    Small_order,
    Order,
    Cart,
    CartProduct
)


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Small_order)
admin.site.register(Order)
admin.site.register(Status)
