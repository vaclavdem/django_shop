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