"""
Личный кабинет: защита авторизацией, история заказов и удаление аккаунта.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Dashboard")
class TestDashboard:

    @allure.title("Visiting the dashboard while logged out redirects to login")
    @pytest.mark.smoke
    @pytest.mark.dashboard
    def test_dashboard_requires_auth_redirect(self, dashboard_page):
        dashboard_page.open()
        assert "login.html" in dashboard_page.current_url

    @allure.title("A logged-in user sees a personalized welcome message and order history")
    @pytest.mark.smoke
    @pytest.mark.dashboard
    def test_dashboard_shows_welcome_and_orders(self, logged_in_dashboard):
        assert "Test User" in logged_in_dashboard.welcome_text()
        assert logged_in_dashboard.order_count() == 3

    @allure.title("Confirming account deletion logs the user out")
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_delete_account_confirm_logs_out(self, logged_in_dashboard):
        logged_in_dashboard.click_delete_account()
        logged_in_dashboard.accept_alert()
        assert "login.html" in logged_in_dashboard.current_url

    @allure.title("Dismissing the delete-account confirm keeps the user on the dashboard")
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_delete_account_dismiss_stays(self, logged_in_dashboard):
        logged_in_dashboard.click_delete_account()
        logged_in_dashboard.dismiss_alert()
        assert "dashboard.html" in logged_in_dashboard.current_url

    @allure.title("Logging out clears the session and returns to the login page")
    @pytest.mark.dashboard
    def test_logout_clears_session(self, logged_in_dashboard):
        logged_in_dashboard.logout()
        assert "login.html" in logged_in_dashboard.current_url

        logged_in_dashboard.open()  # revisit dashboard directly
        assert "login.html" in logged_in_dashboard.current_url
