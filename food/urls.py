from django.urls import path

from food.api.views import (
    RestaurantListView,
    FoodListView,
    FoodCreateView,
    FoodEditView,
    FoodDeleteView,
)


urlpatterns = [
    path("restaurants/", RestaurantListView.as_view()),
    path("restaurants/<int:pk>/", FoodListView.as_view()),
    path("addfood/", FoodCreateView.as_view()),
    path("food/<int:pk>/change/", FoodEditView.as_view()),
    path("food/<int:pk>/delete/", FoodDeleteView.as_view()),
]
