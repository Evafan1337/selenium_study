from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CheckoutPage(BasePage):
    FULL_NAME = (By.ID, "full-name")
    ADDRESS = (By.ID, "address")
    CITY = (By.ID, "city")
    ZIP = (By.ID, "zip")
    TO_STEP_2_BTN = (By.ID, "to-step-2")
    TO_STEP_3_BTN = (By.ID, "to-step-3")
    PLACE_ORDER_BTN = (By.ID, "place-order-btn")

    PAYMENT_CARD = (By.CSS_SELECTOR, "[data-testid=payment-card]")
    PAYMENT_PAYPAL = (By.CSS_SELECTOR, "[data-testid=payment-paypal]")
    PAYMENT_CASH = (By.CSS_SELECTOR, "[data-testid=payment-cash]")
    CARD_FIELDS = (By.ID, "card-fields")

    EMPTY_WARNING = (By.ID, "cart-empty-warning")
    ORDER_NUMBER = (By.ID, "order-number")
    STEP_PANEL_1 = (By.ID, "step-1")
    STEP_PANEL_2 = (By.ID, "step-2")
    STEP_PANEL_3 = (By.ID, "step-3")

    def open(self, path: str = "checkout.html") -> "CheckoutPage":
        super().open(path)
        return self

    def fill_shipping(self, name: str, address: str, city: str, zip_code: str) -> "CheckoutPage":
        self.type_text(self.FULL_NAME, name)
        self.type_text(self.ADDRESS, address)
        self.type_text(self.CITY, city)
        self.type_text(self.ZIP, zip_code)
        return self

    def continue_to_payment(self) -> "CheckoutPage":
        self.click(self.TO_STEP_2_BTN)
        return self

    def choose_payment_method(self, method: str) -> "CheckoutPage":
        locator = {"card": self.PAYMENT_CARD, "paypal": self.PAYMENT_PAYPAL, "cash": self.PAYMENT_CASH}[method]
        self.click(locator)
        return self

    def is_card_fields_visible(self) -> bool:
        return self.is_displayed(self.CARD_FIELDS)

    def continue_to_review(self) -> "CheckoutPage":
        self.click(self.TO_STEP_3_BTN)
        return self

    def place_order_and_accept(self) -> "CheckoutPage":
        self.click(self.PLACE_ORDER_BTN)
        self.accept_alert()
        return self

    def place_order_and_dismiss(self) -> "CheckoutPage":
        self.click(self.PLACE_ORDER_BTN)
        self.dismiss_alert()
        return self

    def is_empty_warning_visible(self) -> bool:
        return self.is_displayed(self.EMPTY_WARNING)

    def order_number(self) -> str:
        return self.get_text(self.ORDER_NUMBER)

    def active_step_panel_id(self) -> str:
        for locator in (self.STEP_PANEL_1, self.STEP_PANEL_2, self.STEP_PANEL_3):
            element = self.find(locator)
            if "active" in element.get_attribute("class"):
                return element.get_attribute("id")
        return ""
