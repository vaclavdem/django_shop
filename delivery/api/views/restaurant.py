from rest_framework import generics, permissions

from delivery.models import Restaurant

from delivery.api.serializers.restaurant import RestaurantListSerializer


class RestaurantListView(generics.ListAPIView):
    """Вывод списка ресторанов"""
    serializer_class = RestaurantListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Restaurant.objects.filter(draft=False)