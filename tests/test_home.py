"""
Главная страница: сетка популярных товаров и клиентский поиск.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Home page")
class TestHomePage:

    @allure.title("Home page loads with the expected title")
    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_page_title(self, home_page):
        home_page.open()
        assert "ShopEasy" in home_page.title

    @allure.title("Featured grid shows all six seed products")
    @pytest.mark.catalog
    def test_product_cards_displayed(self, home_page):
        home_page.open()
        assert len(home_page.product_names()) == 6

    @allure.title("Searching filters the visible product cards")
    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_search_filters_products(self, home_page):
        home_page.open()
        with allure.step("Search for 'keyboard'"):
            home_page.search("keyboard")
        names = home_page.product_names()
        assert len(names) == 1
        assert "Keyboard" in names[0]

    @allure.title("Searching for a non-existent product shows the empty-state message")
    @pytest.mark.catalog
    def test_search_no_results(self, home_page):
        home_page.open()
        home_page.search("nonexistent-gadget-xyz")
        assert home_page.has_no_results_message()

    @allure.title("Clicking a product card navigates to its detail page")
    @pytest.mark.catalog
    def test_navigate_to_product_details(self, home_page):
        home_page.open()
        product_page = home_page.open_product(index=0)
        assert product_page.name != ""
