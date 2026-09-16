"""
04 — Page Object И фикстуры вместе — так же устроены tests/ и conftest.py
в этом проекте, просто собраны здесь в один файл для сравнения.

Это тот же сценарий, что и в файлах 01–03, но теперь и подготовка, и сама
проверка сведены к минимуму: setup/teardown — в фикстурах, работа со
страницей — в Page Object, а тест — это 2-3 строки читаемого сценария.

Сравните объём этого файла с файлом 01: разница — это и есть то, что
фреймворк тестирования экономит на каждом новом тесте.
"""

import pytest

from framework.pages.login_page import LoginPage
from framework.utils.driver_factory import build_driver
from framework.utils.local_server import LocalSiteServer


@pytest.fixture(scope="module")
def site_server():
    server = LocalSiteServer().start()
    yield server
    server.stop()


@pytest.fixture
def driver(site_server):
    drv = build_driver()
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver, site_server):
    # фикстура может зависеть от других фикстур — pytest сам подставит driver и site_server
    return LoginPage(driver, site_server.url())


def test_successful_login(login_page):
    login_page.open()
    dashboard = login_page.login("test@example.com", "Password123")
    assert "Test User" in dashboard.welcome_text()


def test_invalid_login_shows_error(login_page):
    login_page.open()
    login_page.login_expecting_error("wrong@example.com", "wrongpass")
    assert login_page.is_error_visible()
    assert "email or password" in login_page.error_text().lower()
