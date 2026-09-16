from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage
from framework.pages.dashboard_page import DashboardPage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    REMEMBER_CHECKBOX = (By.ID, "remember")
    SUBMIT_BTN = (By.ID, "login-btn")
    ERROR_MSG = (By.ID, "login-error")
    REGISTER_LINK = (By.LINK_TEXT, "Create one")

    def open(self, path: str = "login.html") -> "LoginPage":
        super().open(path)
        return self

    def login(self, email: str, password: str) -> DashboardPage:
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)
        return DashboardPage(self.driver, self.base_url)

    def login_expecting_error(self, email: str, password: str) -> "LoginPage":
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)
        return self

    def toggle_remember_me(self) -> "LoginPage":
        self.click(self.REMEMBER_CHECKBOX)
        return self

    def is_remember_me_checked(self) -> bool:
        return self.find(self.REMEMBER_CHECKBOX).is_selected()

    def is_error_visible(self) -> bool:
        return self.is_displayed(self.ERROR_MSG)

    def error_text(self) -> str:
        return self.get_text(self.ERROR_MSG)
