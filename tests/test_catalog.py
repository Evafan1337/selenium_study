"""
Каталог: фильтр категорий, диапазон цен и сортировка. Все операции динамически
перестраивают сетку товаров и проверяют ожидание содержимого.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Catalog")
class TestCatalog:

    @allure.title("Filtering by category narrows the result count")
    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_category_filter(self, catalog_page):
        catalog_page.open()
        assert catalog_page.result_count() == 6
        catalog_page.filter_by_category("audio")
        assert catalog_page.result_count() == 1

    @allure.title("Lowering the max price slider hides expensive products")
    @pytest.mark.catalog
    def test_price_range_slider(self, catalog_page):
        catalog_page.open()
        catalog_page.set_max_price(60)
        prices = catalog_page.product_prices()
        assert prices, "expected at least one product under $60"
        assert all(p <= 60 for p in prices)

    @allure.title("Sorting by price ascending orders the visible products")
    @pytest.mark.catalog
    def test_sort_price_ascending(self, catalog_page):
        catalog_page.open()
        catalog_page.sort_by("price-asc")
        prices = catalog_page.product_prices()
        assert prices == sorted(prices)

    @allure.title("Sorting by price descending orders the visible products")
    @pytest.mark.catalog
    def test_sort_price_descending(self, catalog_page):
        catalog_page.open()
        catalog_page.sort_by("price-desc")
        prices = catalog_page.product_prices()
        assert prices == sorted(prices, reverse=True)
