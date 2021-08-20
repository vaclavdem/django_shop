from django.urls import path

from delivery.api.views import (
    restaurant,
    report,
    order,
    food,
    cartproduct
)


urlpatterns = [
    path("restaurants/", restaurant.RestaurantListView.as_view()),
    path("restaurants/<int:pk>/", food.FoodListView.as_view()),
    path("order/create/", order.OrderCreateView.as_view()),
    path("order/user/", order.OrderListUserView.as_view()),
    path("order/delivery/", order.OrderListView.as_view()),
    path("order/delivery/taken/", order.OrderTakenView.as_view()),
    path("order/delivery/<int:pk>/", order.OrderEditView.as_view()),
    path("order/delivery/<int:pk>/take/", order.OrderTakeView.as_view()),
    path("order/delivery/<int:pk>/complete/", order.OrderDeliveredView.as_view()),
    path("order/user/<int:pk>/delete/", order.OrderDeleteUserView.as_view()),
    path("order/user/<int:pk>/change/", order.OrderChangeUserView.as_view()),
    path("addfood/", food.FoodCreateView.as_view()),
    path("food/<int:pk>/change/", food.FoodEditView.as_view()),
    path("food/<int:pk>/delete/", food.FoodDeleteView.as_view()),
    path("reports/", report.ReportsView.as_view()),
    path("reports/<int:pk>/create/", report.ReportCreateView.as_view()),
    path("reports/<int:pk>/delete/", report.ReportDestroyView.as_view()),
    path("foodaddtocart/<int:pk>/", cartproduct.AddFoodToCartView.as_view()),
    path("cart/", cartproduct.CartView.as_view()),
    path("cart/<int:pk>/delete/", cartproduct.CartProductDestroyView.as_view()),
]
