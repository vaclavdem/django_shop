from django.contrib import admin

from .models import (
    Food,
    Restaurant,
    Users,
    Discounts,
    Category
)


admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Users)
admin.site.register(Discounts)