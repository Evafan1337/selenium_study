"""
Вход: корректные и ошибочные данные, флажок «Запомнить меня».
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Authentication")
class TestLogin:

    @allure.title("Valid credentials log the user in and land on the dashboard")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login(self, login_page):
        login_page.open()
        dashboard = login_page.login("test@example.com", "Password123")
        assert "Test User" in dashboard.welcome_text()

    @allure.title("Invalid credentials show an inline error and stay on the login page")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_invalid_login_shows_error(self, login_page):
        login_page.open()
        login_page.login_expecting_error("wrong@example.com", "wrongpass")
        assert login_page.is_error_visible()
        assert "email or password" in login_page.error_text().lower()

    @allure.title("The 'remember me' checkbox toggles correctly")
    @pytest.mark.login
    def test_remember_me_checkbox(self, login_page):
        login_page.open()
        assert not login_page.is_remember_me_checked()
        login_page.toggle_remember_me()
        assert login_page.is_remember_me_checked()

    @allure.title("The register link navigates to the registration page")
    @pytest.mark.login
    def test_register_link_navigates(self, login_page):
        login_page.open()
        login_page.click(login_page.REGISTER_LINK)
        assert "register.html" in login_page.current_url
