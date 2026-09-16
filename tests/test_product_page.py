"""
Карточка товара: выбор количества, добавление в корзину и вкладки.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Product page")
class TestProductPage:

    @allure.title("Adding a product to the cart updates the header badge")
    @pytest.mark.smoke
    @pytest.mark.product
    def test_add_to_cart_updates_badge(self, product_page):
        product_page.open_by_id(1)
        product_page.add_to_cart()
        assert product_page.is_added_message_visible()
        assert product_page.cart_badge_count() == 1

    @allure.title("Selecting a quantity before adding multiplies the cart count")
    @pytest.mark.product
    def test_quantity_selection(self, product_page):
        product_page.open_by_id(2)
        product_page.set_quantity(3)
        product_page.add_to_cart()
        assert product_page.cart_badge_count() == 3

    @allure.title("Switching tabs shows specifications instead of the description")
    @pytest.mark.product
    def test_tabs_switch_content(self, product_page):
        product_page.open_by_id(3)
        assert product_page.is_description_panel_active()
        product_page.open_specs_tab()
        assert product_page.is_specs_panel_active()
        assert not product_page.is_description_panel_active()

    @allure.title("Opening an unknown product id shows the not-found state")
    @pytest.mark.regression
    @pytest.mark.product
    def test_unknown_product_id(self, product_page):
        product_page.open_by_id(999)
        assert product_page.is_not_found()
