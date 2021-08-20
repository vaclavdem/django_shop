from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Users(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_active(self):
        return True


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Discounts(models.Model):
    """Типы скидок"""
    name = models.CharField("Тип скидки", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип скидки"
        verbose_name_plural = "Типы скидок"


class Restaurant(models.Model):
    """Рестораны"""
    title = models.CharField("Ресторан", max_length=150)
    cooking_time = models.CharField("Среднее время приготовления", max_length=100)
    min_price = models.PositiveIntegerField("Минимальная цена", default=5,
                                         help_text="указывать сумму в рублях")
    category = models.ManyToManyField(Category, verbose_name="Категория")
    address = models.TextField("Адресс", max_length=100, default="")
    email = models.EmailField("Email", default="")
    draft = models.BooleanField("Черновик", default=False)
    restaurant_owner = models.ForeignKey(Users, verbose_name="Пользователь", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"


class Food(models.Model):
    """Еда"""
    name = models.CharField("Еда", max_length=150)
    description = models.TextField("Описание", default="")
    price = models.FloatField("Цена", default=5,
                                            help_text="указывать сумму в рублях, без скидки")
    type_discount = models.ForeignKey(Discounts, verbose_name="Тип скидки", on_delete=models.CASCADE, default=1)
    percent = models.PositiveIntegerField("Процент скидки", default=0,
                                            help_text="работает тольки при типе скидке : 'Скидка'")
    discounted_price = models.FloatField("Конечная цена", default=5,
                                                   help_text="Вписать любую, потом изменится")
    restaurant = models.ForeignKey(Restaurant, verbose_name="Ресторан", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Еда"
        verbose_name_plural = "Еда"

    def save(self, *args, **kwargs):
        if self.type_discount.name == "Скидка":
            self.discounted_price = self.price * ((100.0 - self.percent) / 100.0)
        else:
            self.discounted_price = self.price
        super().save(*args, **kwargs)


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


class Report(models.Model):
    """Жалобы"""
    email = models.EmailField("Email")
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, default=9)
    comment = models.TextField("Коментарий", max_length=5000, default="")

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"
