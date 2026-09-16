"""
Регистрация: успешный сценарий и три клиентские проверки данных.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Registration")
class TestRegistration:

    @allure.title("Filling every field correctly registers the account")
    @pytest.mark.smoke
    @pytest.mark.registration
    def test_successful_registration(self, register_page):
        register_page.open()
        register_page.fill_basic_info("Ada", "Lovelace", "ada@example.com")
        register_page.fill_passwords("Sup3rSecret!", "Sup3rSecret!")
        register_page.select_gender_female()
        register_page.select_country("Germany")
        register_page.accept_terms()
        register_page.submit()
        assert register_page.is_success_visible()

    @allure.title("Mismatched passwords are rejected with an inline error")
    @pytest.mark.regression
    @pytest.mark.registration
    def test_password_mismatch_validation(self, register_page):
        register_page.open()
        register_page.fill_basic_info("Grace", "Hopper", "grace@example.com")
        register_page.fill_passwords("Password1", "Password2")
        register_page.accept_terms()
        register_page.submit()
        assert register_page.is_password_error_visible()
        assert not register_page.is_success_visible()

    @allure.title("Submitting without accepting the terms is blocked")
    @pytest.mark.regression
    @pytest.mark.registration
    def test_terms_checkbox_required(self, register_page):
        register_page.open()
        register_page.fill_basic_info("Alan", "Turing", "alan@example.com")
        register_page.fill_passwords("Password1", "Password1")
        register_page.submit()
        assert register_page.is_terms_error_visible()
        assert not register_page.is_success_visible()

    @allure.title("An invalid email format is rejected")
    @pytest.mark.regression
    @pytest.mark.registration
    def test_invalid_email_format(self, register_page):
        register_page.open()
        register_page.fill_basic_info("Linus", "Torvalds", "not-an-email")
        register_page.fill_passwords("Password1", "Password1")
        register_page.accept_terms()
        register_page.submit()
        assert register_page.is_email_error_visible()
