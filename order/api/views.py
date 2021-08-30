from food.service.mixins import CartMixin

from rest_framework import generics, permissions
from order.service.utils import recalc_cart

from food.models import Food, Users
from order.models import CartProduct, Cart, Small_order, Order

from rest_framework.response import Response
from order.service.utils import logic

from .serializers import (
    AddToCartSerializer,
    CartSerializer,
    OrderCreateSerializer,
    OrderEditSerializer,
    OrderUserListSerializer,
    OrderEditUserSerializer,
    OrderListSerializer,
    OrderTakeSerializer,
    OrderDeliveredSerializer,
)

from order.service.permissions import IsDeliveryUser

from order.service.tasks import send_email

from datetime import datetime
import time


class AddFoodToCartView(CartMixin, generics.CreateAPIView):
    """Добавление продукта в корзину"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def perform_create(self, serializer):
        food = Food.objects.get(id=self.kwargs.get('pk'))
        serializer.save(user_id=self.request.user.id, food=food, restaurant=food.restaurant)
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        product = CartProduct.objects.filter(user_id=self.request.user.id).last()
        cart.food.add(product)
        recalc_cart(cart)


class CartView(generics.ListAPIView):
    """Корзина"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        cartproduct = cart.food.all()
        queryset = cartproduct
        return queryset


class CartProductDestroyView(generics.RetrieveDestroyAPIView):
    """Удаление продукта из корзины"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        cartproduct = cart.food.all()
        queryset = cartproduct
        return queryset

    def perform_create(self, serializer):
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        recalc_cart(cart)


class OrderListView(generics.ListAPIView):
    """Просмотр заказов доставщиками"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        queryset = Small_order.objects.filter(is_active=False)
        return queryset


class OrderEditView(CartMixin, generics.RetrieveUpdateAPIView):
    """Изменение статуса заказа"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderEditSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        queryset = Small_order.objects.filter(is_active=True, delivery=user)
        order = Small_order.objects.get(id=self.kwargs.get('pk'))
        send_email("Информирование", "Статус вашего заказа изменён", order.email)
        return queryset


class OrderCreateView(CartMixin, generics.CreateAPIView):
    """Создание заказа"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        logic(self, serializer)
        send_email("Информирование", "С вашего устройства создали заказ", self.request.data.get("email"))


class OrderTakeView(CartMixin, generics.RetrieveUpdateAPIView):
    """Взятие заказа"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderTakeSerializer
    queryset = Small_order.objects.filter(is_active=False)

    def put(self, request, *args, **kwargs):
        order = Small_order.objects.get(id=self.kwargs.get('pk'))
        send_email("Заказ", "Курьер принял ваш заказ", order.email)
        user = Users.objects.get(user=self.request.user)
        order.delivery = user
        order.is_active = True
        order.save()
        return Response(request.data)


class OrderDeliveredView(CartMixin, generics.RetrieveUpdateAPIView):
    """Изменение основного статуса заказа"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderDeliveredSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        queryset = Small_order.objects.filter(is_active=True, delivery=user)
        return queryset

    def put(self, request, *args, **kwargs):
        order = Small_order.objects.get(id=self.kwargs.get('pk'))
        send_email("Заказ", "Курьер доставил ваш заказ", order.email)
        order.is_delivered = True
        order.delivered_at = time.mktime(datetime.now().timetuple())
        order.save()
        return Response(request.data)


class OrderTakenView(generics.ListAPIView):
    """просмотр взятых заказов"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        queryset = Small_order.objects.filter(delivery=user, is_active=True)
        return queryset


class OrderListUserView(generics.ListAPIView):
    """просмотр заказов клиентами"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderUserListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset


class OrderDeleteUserView(generics.RetrieveDestroyAPIView):
    """Удаление заказа клиентом"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderUserListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset


class OrderChangeUserView(generics.RetrieveUpdateAPIView):
    """Редактирование заказа клиентом"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderEditUserSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset