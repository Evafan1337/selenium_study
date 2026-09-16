from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class RegisterPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    EMAIL = (By.ID, "reg-email")
    PASSWORD = (By.ID, "reg-password")
    CONFIRM_PASSWORD = (By.ID, "confirm-password")
    BIRTH_DATE = (By.ID, "birth-date")
    GENDER_FEMALE = (By.CSS_SELECTOR, "[data-testid=gender-female]")
    GENDER_MALE = (By.CSS_SELECTOR, "[data-testid=gender-male]")
    COUNTRY_SELECT = (By.ID, "country")
    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    TERMS_CHECKBOX = (By.ID, "terms")
    SUBMIT_BTN = (By.ID, "register-btn")

    EMAIL_ERROR = (By.ID, "email-error")
    PASSWORD_ERROR = (By.ID, "password-error")
    TERMS_ERROR = (By.ID, "terms-error")
    SUCCESS_MSG = (By.ID, "register-success")

    def open(self, path: str = "register.html") -> "RegisterPage":
        super().open(path)
        return self

    def fill_basic_info(self, first_name: str, last_name: str, email: str) -> "RegisterPage":
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.EMAIL, email)
        return self

    def fill_passwords(self, password: str, confirm: str) -> "RegisterPage":
        self.type_text(self.PASSWORD, password)
        self.type_text(self.CONFIRM_PASSWORD, confirm)
        return self

    def select_gender_female(self) -> "RegisterPage":
        self.click(self.GENDER_FEMALE)
        return self

    def select_country(self, country_name: str) -> "RegisterPage":
        self.select_by_visible_text(self.COUNTRY_SELECT, country_name)
        return self

    def accept_terms(self) -> "RegisterPage":
        self.click(self.TERMS_CHECKBOX)
        return self

    def submit(self) -> "RegisterPage":
        self.click(self.SUBMIT_BTN)
        return self

    def is_email_error_visible(self) -> bool:
        return self.is_displayed(self.EMAIL_ERROR)

    def is_password_error_visible(self) -> bool:
        return self.is_displayed(self.PASSWORD_ERROR)

    def is_terms_error_visible(self) -> bool:
        return self.is_displayed(self.TERMS_ERROR)

    def is_success_visible(self) -> bool:
        return self.is_displayed(self.SUCCESS_MSG)
