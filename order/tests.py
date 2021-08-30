from django.test import TestCase
from rest_framework.test import APIRequestFactory

from django.contrib.auth import get_user_model

from food.models import Food, Restaurant, Users, Discounts
from order.models import CartProduct, Cart, Status

from order.service.utils import recalc_cart

from order.api.views import AddFoodToCartView

User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.customer = User.objects.create(username="testuser", password="password", is_active=True)
        self.user = Users.objects.create(user=self.customer, id=1)
        self.restaurant = Restaurant.objects.create(
            title="Sea",
            cooking_time="50 мин",
            min_price=2,
            address="Комсомольская, 17",
            email="test@gmail.com",
            restaurant_owner=self.user,
        )
        self.no_discount = Discounts.objects.create(name="Нету")
        self.discount_1 = Discounts.objects.create(name="Скидка")
        self.discount_2 = Discounts.objects.create(name="1+1")
        self.food_1 = Food.objects.create(
            name="Филадельфия",
            description="Филе лосося, авокадо, сливочный сыр, нори, рис. 8 штук",
            price=17.9,
            type_discount=self.no_discount,
            restaurant=self.restaurant,
            id=1,
        )
        self.food_2 = Food.objects.create(
            name="Самурай",
            description="Филе угря, лосося, огурец, сливочный сыр, соус терияки, кунжут, нори, рис. 8 штук",
            price=19.2,
            type_discount=self.discount_1,
            percent=50,
            restaurant=self.restaurant,
            id=2
        )
        self.food_3 = Food.objects.create(
            name="Аляска",
            description="Тигровая креветка, огурец, икра летучей рыбы, сливочный сыр, нори, рис. 8 штук",
            price=16.9,
            type_discount=self.discount_2,
            restaurant=self.restaurant,
            id=3
        )
        self.cart = Cart.objects.create(user=self.user)
        self.status = Status.objects.create(name="Ожидание")
        self.cart_product_1 = CartProduct.objects.create(
            user_id=1,
            food=self.food_1,
            qty=5,
            restaurant=self.restaurant
        )
        self.cart_product_2 = CartProduct.objects.create(
            user_id=self.user.id,
            food=self.food_2,
            qty=5,
            restaurant=self.restaurant
        )
        self.cart_product_3 = CartProduct.objects.create(
            user_id=self.user.id,
            food=self.food_3,
            qty=5,
            restaurant=self.restaurant
        )

    def test_add_to_cart(self):
        self.cart.food.add(self.cart_product_1, self.cart_product_2, self.cart_product_3)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product_1, self.cart.food.all())
        self.assertIn(self.cart_product_2, self.cart.food.all())
        self.assertIn(self.cart_product_3, self.cart.food.all())
        self.assertEqual(self.cart.food.count(), 3)
        self.assertEqual(self.cart.final_price, 188.2)

    def test_response_from_add_to_cart_view(self):
        self.factory = APIRequestFactory()
        view = AddFoodToCartView().as_view()
        request = self.factory.post('http://127.0.0.1:8000/api/v1/foodaddtocart/1/', {'qty': 3}, format='json')
        request.user = self.customer
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 201)
