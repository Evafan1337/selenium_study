"""
Общие фикстуры pytest.

- `site_server` один раз запускает сервер со статическим сайтом.
- `driver` создаёт новый браузер для каждого теста и затем закрывает его.
- `base_url` формирует адрес на основе `site_server`.
- При падении сохраняется скриншот и прикладывается к отчёту Allure.

Фикстуры Page Object объединяют `driver` и `base_url`, устраняя повторения.
"""

import os
from pathlib import Path

import allure
import pytest

from framework.pages.cart_page import CartPage
from framework.pages.catalog_page import CatalogPage
from framework.pages.checkout_page import CheckoutPage
from framework.pages.dashboard_page import DashboardPage
from framework.pages.home_page import HomePage
from framework.pages.login_page import LoginPage
from framework.pages.playground_page import PlaygroundPage
from framework.pages.product_page import ProductPage
from framework.pages.register_page import RegisterPage
from framework.utils.driver_factory import build_driver
from framework.utils.local_server import LocalSiteServer

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots"


@pytest.fixture(scope="session")
def site_server():
    server = LocalSiteServer().start()
    yield server
    server.stop()


@pytest.fixture(scope="session")
def base_url(site_server) -> str:
    return site_server.url()


@pytest.fixture
def driver():
    drv = build_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """При падении сохранить скриншот и приложить его к Allure."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"
    drv.save_screenshot(str(screenshot_path))

    try:
        allure.attach.file(str(screenshot_path), name="failure-screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass  # Если Allure не активен, достаточно файла на диске.


# ---------------- Фикстуры Page Object ----------------


@pytest.fixture
def home_page(driver, base_url) -> HomePage:
    return HomePage(driver, base_url)


@pytest.fixture
def catalog_page(driver, base_url) -> CatalogPage:
    return CatalogPage(driver, base_url)


@pytest.fixture
def login_page(driver, base_url) -> LoginPage:
    return LoginPage(driver, base_url)


@pytest.fixture
def register_page(driver, base_url) -> RegisterPage:
    return RegisterPage(driver, base_url)


@pytest.fixture
def product_page(driver, base_url) -> ProductPage:
    return ProductPage(driver, base_url)


@pytest.fixture
def cart_page(driver, base_url) -> CartPage:
    return CartPage(driver, base_url)


@pytest.fixture
def checkout_page(driver, base_url) -> CheckoutPage:
    return CheckoutPage(driver, base_url)


@pytest.fixture
def dashboard_page(driver, base_url) -> DashboardPage:
    return DashboardPage(driver, base_url)


@pytest.fixture
def playground_page(driver, base_url) -> PlaygroundPage:
    return PlaygroundPage(driver, base_url)


@pytest.fixture
def logged_in_driver(driver, base_url):
    """Драйвер с выполненным входом и открытым личным кабинетом."""
    login_page = LoginPage(driver, base_url).open()
    login_page.login("test@example.com", "Password123")
    return driver


@pytest.fixture
def logged_in_dashboard(logged_in_driver, base_url) -> DashboardPage:
    return DashboardPage(logged_in_driver, base_url)
