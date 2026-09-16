from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class DashboardPage(BasePage):
    WELCOME_MSG = (By.ID, "welcome-msg")
    ORDERS_TABLE = (By.CSS_SELECTOR, "[data-testid=orders-table]")
    ORDER_ROWS = (By.CSS_SELECTOR, "[data-testid=orders-body] tr")
    DELETE_ACCOUNT_BTN = (By.ID, "delete-account-btn")
    LOGOUT_LINK = (By.ID, "logout-link")

    def open(self, path: str = "dashboard.html") -> "DashboardPage":
        super().open(path)
        return self

    def welcome_text(self) -> str:
        return self.get_text(self.WELCOME_MSG)

    def order_count(self) -> int:
        return len(self.find_all(self.ORDER_ROWS))

    def click_delete_account(self) -> "DashboardPage":
        self.click(self.DELETE_ACCOUNT_BTN)
        return self

    def logout(self) -> None:
        self.click(self.LOGOUT_LINK)
