from delivery.service.mixins import CartMixin

from rest_framework import generics, permissions
from delivery.service.utils import recalc_cart

from delivery.models import Food, Users, CartProduct, Cart

from delivery.api.serializers.cartproduct import AddToCartSerializer, CartSerializer

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