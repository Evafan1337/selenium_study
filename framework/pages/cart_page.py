from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CartPage(BasePage):
    EMPTY_MSG = (By.ID, "empty-cart-msg")
    CART_ROWS = (By.CSS_SELECTOR, "[data-testid=cart-row]")
    TOTAL = (By.ID, "cart-total")
    CHECKOUT_BTN = (By.ID, "checkout-btn")

    def open(self, path: str = "cart.html") -> "CartPage":
        super().open(path)
        return self

    def is_empty(self) -> bool:
        return self.is_displayed(self.EMPTY_MSG)

    def row_count(self) -> int:
        return len(self.find_all(self.CART_ROWS))

    def total(self) -> str:
        return self.get_text(self.TOTAL)

    def set_quantity(self, product_id: int, quantity: int) -> "CartPage":
        locator = (By.CSS_SELECTOR, f"[data-testid=cart-qty-input][data-product-id='{product_id}']")
        field = self.find(locator)
        # Метод clear() отправляет событие change, после которого cart.js заново
        # строит таблицу. Ссылка field сразу устаревает, поэтому задаём значение
        # одним вызовом JavaScript.
        self.driver.execute_script(
            """
            const el = arguments[0];
            el.value = arguments[1];
            el.dispatchEvent(new Event('change', {bubbles: true}));
            """,
            field,
            quantity,
        )
        return self

    def remove_product(self, product_id: int) -> "CartPage":
        locator = (By.CSS_SELECTOR, f"[data-testid=cart-remove-btn][data-product-id='{product_id}']")
        self.click(locator)
        return self

    def subtotal_for(self, product_id: int) -> str:
        row = self.find((By.CSS_SELECTOR, f"[data-testid=cart-row][data-product-id='{product_id}']"))
        return row.find_element(By.CSS_SELECTOR, "[data-testid=cart-row-subtotal]").text

    def go_to_checkout(self):
        from framework.pages.checkout_page import CheckoutPage

        self.click(self.CHECKOUT_BTN)
        return CheckoutPage(self.driver, self.base_url)
