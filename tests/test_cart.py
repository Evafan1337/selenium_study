"""
Корзина: количество, удаление, пустое состояние и итоговая сумма.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Cart")
class TestCart:

    @allure.title("A freshly opened cart is empty")
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_empty_cart_message(self, cart_page):
        cart_page.open()
        assert cart_page.is_empty()

    @allure.title("Adding a product from the product page makes it appear in the cart")
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_product_appears_in_cart(self, product_page, cart_page):
        product_page.open_by_id(1).add_to_cart()
        cart_page.open()
        assert cart_page.row_count() == 1

    @allure.title("Changing the quantity in the cart recalculates the row subtotal and total")
    @pytest.mark.cart
    def test_update_quantity_recalculates_total(self, product_page, cart_page):
        product_page.open_by_id(5).add_to_cart()  # $89.99
        cart_page.open()
        cart_page.set_quantity(5, 2)
        assert cart_page.subtotal_for(5) == "$179.98"
        assert cart_page.total() == "$179.98"

    @allure.title("Removing the only item empties the cart")
    @pytest.mark.cart
    def test_remove_item_from_cart(self, product_page, cart_page):
        product_page.open_by_id(6).add_to_cart()
        cart_page.open()
        assert cart_page.row_count() == 1
        cart_page.remove_product(6)
        assert cart_page.is_empty()

    @allure.title("Cart total sums multiple distinct products correctly")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_total_sums_multiple_products(self, product_page, cart_page):
        product_page.open_by_id(4).add_to_cart()   # $59.00
        product_page.open_by_id(6).add_to_cart()   # $34.50
        cart_page.open()
        assert cart_page.row_count() == 2
        assert cart_page.total() == "$93.50"
