from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage
from framework.pages.product_page import ProductPage


class HomePage(BasePage):
    SEARCH_INPUT = (By.ID, "search-input")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "[data-testid=product-card]")
    NO_RESULTS_MSG = (By.ID, "no-results-msg")
    VIEW_PRODUCT_LINKS = (By.CSS_SELECTOR, "[data-testid=view-product-btn]")

    def open(self, path: str = "index.html") -> "HomePage":
        super().open(path)
        return self

    def search(self, term: str) -> "HomePage":
        self.type_text(self.SEARCH_INPUT, term)
        return self

    def product_names(self) -> list[str]:
        return [card.find_element(By.CLASS_NAME, "product-name").text for card in self.find_all(self.PRODUCT_CARDS)]

    def has_no_results_message(self) -> bool:
        return self.is_displayed(self.NO_RESULTS_MSG)

    def open_product(self, index: int = 0) -> ProductPage:
        links = self.find_all(self.VIEW_PRODUCT_LINKS)
        links[index].click()
        return ProductPage(self.driver, self.base_url)
