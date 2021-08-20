from rest_framework import serializers

from delivery.models import Restaurant


class RestaurantListSerializer(serializers.ModelSerializer):
    """Список ресторанов"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Restaurant
        fields = ("title", "cooking_time", "min_price", "category")