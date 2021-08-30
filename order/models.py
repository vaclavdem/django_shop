from django.db import models

from food.models import Food, Restaurant, Users


class Status(models.Model):
    """Статусы заказа"""
    name = models.CharField("Статус заказа", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class CartProduct(models.Model):
    """Продукты корзины"""
    user_id = models.PositiveIntegerField("Id пользователя", default=2)
    food = models.ForeignKey(Food, verbose_name="Статус", on_delete=models.CASCADE, default=1)
    qty = models.PositiveIntegerField(default=1, verbose_name="Кол-во")
    final_price = models.FloatField(default=0, verbose_name='Общая цена')
    restaurant = models.ForeignKey(Restaurant, verbose_name="Ресторан", on_delete=models.CASCADE)

    def __int__(self):
        return self.user_id

    class Meta:
        verbose_name = "Продукт для корзины"
        verbose_name_plural = "Продукты для корзины"

    def save(self, *args, **kwargs):
        if self.food.type_discount.name == "1+1" and self.qty % 2 == 0:
            self.final_price = float(self.food.discounted_price) * (self.qty // 2)
        else:
            if self.food.type_discount.name == "1+1" and self.qty % 2 == 1:
                self.final_price = float(self.food.discounted_price) * (self.qty // 2 + 1)
            else:
                self.final_price = float(self.food.discounted_price) * self.qty
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Корзина"""
    user = models.ForeignKey(Users, verbose_name="Пользователь", on_delete=models.CASCADE, default=1)
    food = models.ManyToManyField(CartProduct, verbose_name="Еда", blank=True, related_name='related_cart')
    final_price = models.FloatField(default=0, verbose_name='Общая цена')

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Small_order(models.Model):
    """Разбитые по ресторанам заказы"""
    user = models.ForeignKey(Users, verbose_name="Пользователь", on_delete=models.CASCADE, default=1,
                             related_name="User")
    email = models.EmailField("Email")
    name = models.CharField("Имя", max_length=100)
    fromm = models.TextField("Адресс", max_length=100, default="")
    to = models.TextField("Адрес доставки", max_length=100)
    cart_product = models.ManyToManyField(CartProduct, verbose_name="Еда", blank=True)
    comment = models.TextField("Коментарий", max_length=5000, default="")
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.CASCADE, default=1)
    final_price = models.FloatField(default=0, verbose_name='Общая цена')
    delivery = models.ForeignKey(Users, verbose_name="Доставщик", on_delete=models.CASCADE, default=1,
                                 related_name="Delivery")
    is_active = models.BooleanField("Доставить", default=False)
    is_delivered = models.BooleanField("Доставлен", default=False)
    delivered_at = models.FloatField(default=0, verbose_name='Дата доставки')
    restaurant = models.ForeignKey(Restaurant, verbose_name="Рестораны", on_delete=models.CASCADE, default=1)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = "Раздробленный заказ"
        verbose_name_plural = "Раздробленные заказы"


class Order(models.Model):
    """Заказы"""
    user = models.ForeignKey(Users, verbose_name="Пользователь", on_delete=models.CASCADE, default=1,)
    email = models.EmailField("Email")
    name = models.CharField("Имя", max_length=100)
    to = models.TextField("Адрес доставки", max_length=100)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, default=1)
    view_cart = models.ManyToManyField(CartProduct, verbose_name="Еда", blank=True)
    comment = models.TextField("Коментарий", max_length=5000, default="")
    final_price = models.FloatField(default=0, verbose_name='Общая цена')
    restaurants = models.ManyToManyField(Restaurant, verbose_name="Рестораны", blank=True)
    small_order = models.ManyToManyField(Small_order, verbose_name="Раздробленные заказы", blank=True, default=1)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"