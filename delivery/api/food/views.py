from delivery.service.mixins import CartMixin

from rest_framework import generics, permissions

from .models import Food, Users, Restaurant

from .serializers import FoodSerializer, FoodCreateChangeSerializer, RestaurantListSerializer

from delivery.service.permissions import IsRestaurantUser


class FoodListView(generics.ListAPIView):
    """Вывод списка еды"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FoodSerializer

    def get_queryset(self):
        queryset = Food.objects.filter(restaurant=self.kwargs.get('pk'))
        return queryset


class FoodCreateView(CartMixin, generics.CreateAPIView):
    """Добавление еды"""
    permission_classes = (IsRestaurantUser,)
    serializer_class = FoodCreateChangeSerializer

    def perform_create(self, serializer):
        user = Users.objects.get(user=self.request.user)
        restaurant = Restaurant.objects.get(restaurant_owner=user)
        serializer.save(restaurant=restaurant)


class FoodEditView(generics.RetrieveUpdateAPIView):
    """Редактирование еды"""
    permission_classes = (IsRestaurantUser,)
    serializer_class = FoodCreateChangeSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        restaurant = Restaurant.objects.get(restaurant_owner=user)
        queryset = Food.objects.filter(restaurant=restaurant)
        return queryset


class FoodDeleteView(generics.RetrieveDestroyAPIView):
    """Удаление еды"""
    permission_classes = (IsRestaurantUser,)
    serializer_class = FoodSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        restaurant = Restaurant.objects.get(restaurant_owner=user)
        queryset = Food.objects.filter(restaurant=restaurant)
        return queryset


class RestaurantListView(generics.ListAPIView):
    """Вывод списка ресторанов"""
    serializer_class = RestaurantListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Restaurant.objects.filter(draft=False)