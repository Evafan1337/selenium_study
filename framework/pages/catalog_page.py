from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CatalogPage(BasePage):
    CATEGORY_FILTER = (By.ID, "category-filter")
    MAX_PRICE_RANGE = (By.ID, "max-price")
    SORT_SELECT = (By.ID, "sort-select")
    RESULT_COUNT = (By.ID, "result-count")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "[data-testid=product-card]")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "[data-testid=product-price]")

    def open(self, path: str = "catalog.html") -> "CatalogPage":
        super().open(path)
        return self

    def filter_by_category(self, category_value: str) -> "CatalogPage":
        self.select_by_value(self.CATEGORY_FILTER, category_value)
        return self

    def sort_by(self, sort_value: str) -> "CatalogPage":
        self.select_by_value(self.SORT_SELECT, sort_value)
        return self

    def set_max_price(self, value: int) -> "CatalogPage":
        # Ползунки нестабильно реагируют на send_keys в разных браузерах,
        # поэтому задаём значение через JS и отправляем ожидаемые события.
        slider = self.find(self.MAX_PRICE_RANGE)
        self.driver.execute_script(
            """
            const el = arguments[0];
            const value = arguments[1];
            el.value = value;
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            """,
            slider,
            value,
        )
        return self

    def result_count(self) -> int:
        return int(self.get_text(self.RESULT_COUNT))

    def product_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self.PRODUCT_PRICES)]
