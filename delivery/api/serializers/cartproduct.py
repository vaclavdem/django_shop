from rest_framework import serializers

from delivery.models import CartProduct


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ("food", "qty", "final_price")


class AddToCartSerializer(serializers.ModelSerializer):
    """обавление товара в корзину"""

    class Meta:
        model = CartProduct
        fields = ("qty",)


class CartSerializer(serializers.ModelSerializer):
    """Корзина"""

    class Meta:
        model = CartProduct
        fields = ("qty", "food_id", "final_price")