from django.db import models

from order.models import Order


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
