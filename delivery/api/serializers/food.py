from rest_framework import serializers

from delivery.models import Food


class FoodSerializer(serializers.ModelSerializer):
    """Еда"""

    class Meta:
        model = Food
        fields = ("name", "description", "type_discount", "price", "percent", "discounted_price", "restaurant")


class FoodCreateChangeSerializer(serializers.ModelSerializer):
    """Создание и изменение еды"""

    class Meta:
        model = Food
        fields = ("name", "description", "type_discount", "price", "percent")