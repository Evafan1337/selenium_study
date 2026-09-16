"""
03 — Page Object, но БЕЗ фикстур.

Используем настоящие LoginPage/DashboardPage из framework/pages — те же
классы, что работают в tests/. А вот сервер и драйвер снова создаём и
закрываем руками внутри каждого теста, как в файле 01.

Сравните с 01: тело теста стало заметно короче и читается как сценарий
пользователя, а не как список вызовов Selenium. Но повторяющийся код
setup/teardown из 01 никуда не делся — Page Object его не решает,
он решает только "что делать со страницей", а не "как её поднять и убрать".
"""

from framework.pages.login_page import LoginPage
from framework.utils.driver_factory import build_driver
from framework.utils.local_server import LocalSiteServer


def test_successful_login():
    server = LocalSiteServer().start()
    driver = build_driver()

    # LoginPage прячет внутри себя локаторы и низкоуровневые вызовы Selenium
    login_page = LoginPage(driver, server.url())
    login_page.open()
    # login() сам заполняет форму, кликает и возвращает уже DashboardPage
    dashboard = login_page.login("test@example.com", "Password123")

    assert "Test User" in dashboard.welcome_text()

    driver.quit()
    server.stop()


def test_invalid_login_shows_error():
    server = LocalSiteServer().start()
    driver = build_driver()

    login_page = LoginPage(driver, server.url())
    login_page.open()
    # login_expecting_error() не переходит на другую страницу — остаёмся на LoginPage
    login_page.login_expecting_error("wrong@example.com", "wrongpass")

    assert login_page.is_error_visible()
    assert "email or password" in login_page.error_text().lower()

    driver.quit()
    server.stop()
