from django.urls import path

from order.api.views import (
    OrderCreateView,
    OrderListUserView,
    OrderListView,
    OrderTakenView,
    OrderEditView,
    OrderTakeView,
    OrderDeliveredView,
    OrderDeleteUserView,
    OrderChangeUserView,
    AddFoodToCartView,
    CartView,
    CartProductDestroyView,
)


urlpatterns = [
    path("order/create/", OrderCreateView.as_view()),
    path("order/user/", OrderListUserView.as_view()),
    path("order/delivery/", OrderListView.as_view()),
    path("order/delivery/taken/", OrderTakenView.as_view()),
    path("order/delivery/<int:pk>/", OrderEditView.as_view()),
    path("order/delivery/<int:pk>/take/", OrderTakeView.as_view()),
    path("order/delivery/<int:pk>/complete/", OrderDeliveredView.as_view()),
    path("order/user/<int:pk>/delete/", OrderDeleteUserView.as_view()),
    path("order/user/<int:pk>/change/", OrderChangeUserView.as_view()),
    path("foodaddtocart/<int:pk>/", AddFoodToCartView.as_view()),
    path("cart/", CartView.as_view()),
    path("cart/<int:pk>/delete/", CartProductDestroyView.as_view()),
]
