from rest_framework import serializers

from .models import Food, Restaurant


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


class RestaurantListSerializer(serializers.ModelSerializer):
    """Список ресторанов"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Restaurant
        fields = ("title", "cooking_time", "min_price", "category")