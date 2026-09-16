from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class ProductPage(BasePage):
    NAME = (By.ID, "product-name")
    PRICE = (By.ID, "product-price")
    QUANTITY_SELECT = (By.ID, "quantity-select")
    ADD_TO_CART_BTN = (By.ID, "add-to-cart-btn")
    ADDED_MSG = (By.ID, "added-msg")
    NOT_FOUND = (By.ID, "product-not-found")

    TAB_DESCRIPTION = (By.CSS_SELECTOR, "[data-testid=tab-description]")
    TAB_SPECS = (By.CSS_SELECTOR, "[data-testid=tab-specs]")
    TAB_REVIEWS = (By.CSS_SELECTOR, "[data-testid=tab-reviews]")
    PANEL_DESCRIPTION = (By.ID, "panel-description")
    PANEL_SPECS = (By.ID, "panel-specs")
    PANEL_REVIEWS = (By.ID, "panel-reviews")

    def open_by_id(self, product_id: int) -> "ProductPage":
        self.open(f"product.html?id={product_id}")
        return self

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    def set_quantity(self, quantity: int) -> "ProductPage":
        self.select_by_value(self.QUANTITY_SELECT, str(quantity))
        return self

    def add_to_cart(self) -> "ProductPage":
        self.click(self.ADD_TO_CART_BTN)
        return self

    def is_added_message_visible(self) -> bool:
        return self.is_displayed(self.ADDED_MSG)

    def open_specs_tab(self) -> "ProductPage":
        self.click(self.TAB_SPECS)
        return self

    def open_reviews_tab(self) -> "ProductPage":
        self.click(self.TAB_REVIEWS)
        return self

    def is_specs_panel_active(self) -> bool:
        return "active" in self.find(self.PANEL_SPECS).get_attribute("class")

    def is_description_panel_active(self) -> bool:
        return "active" in self.find(self.PANEL_DESCRIPTION).get_attribute("class")

    def is_not_found(self) -> bool:
        return self.is_displayed(self.NOT_FOUND)

    def cart_badge_count(self) -> int:
        return int(self.get_text((By.ID, "cart-count")))
