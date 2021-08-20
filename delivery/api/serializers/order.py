from rest_framework import serializers

from delivery.models import Order, Small_order
from .cartproduct import CartProductSerializer


class OrderCreateSerializer(serializers.ModelSerializer):
    """Добавление заказа"""

    class Meta:
        model = Order
        fields = ("email", "name", "to", "comment")


class OrderListSerializer(serializers.ModelSerializer):
    """Список заказов"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    restaurant = serializers.SlugRelatedField(slug_field="title", read_only=True)
    cart_product = CartProductSerializer(many=True)

    class Meta:
        model = Small_order
        fields = ("id", "name", "comment", "fromm", "to", "cart_product", "final_price", "status", "restaurant")


class OrderEditSerializer(serializers.ModelSerializer):
    """Изменение статусат заказа"""

    class Meta:
        model = Small_order
        fields = ("status",)


class OrderDeliveredSerializer(serializers.ModelSerializer):
    """Изменение заказа"""

    class Meta:
        model = Small_order
        fields = ("is_delivered",)


class OrderTakeSerializer(serializers.ModelSerializer):
    """Принятие заказа"""

    class Meta:
        model = Small_order
        fields = ("is_active",)


class OrderEditUserSerializer(serializers.ModelSerializer):
    """Изменение заказа"""

    class Meta:
        model = Small_order
        fields = ("comment", "to",)


class OrderProductUserListSerializer(serializers.ModelSerializer):
    """Подробная информация по маленькому заказу"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    restaurant = serializers.SlugRelatedField(slug_field="title", read_only=True)
    cart_product = CartProductSerializer(many=True)

    class Meta:
        model = Small_order
        fields = ("cart_product", "final_price", "status", "is_active", "is_delivered", "restaurant")


class OrderUserListSerializer(serializers.ModelSerializer):
    """Список заказов для пользователя"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    small_order = OrderProductUserListSerializer(many=True)

    class Meta:
        model = Order
        fields = ("comment", "to", "small_order", "final_price", "status")