"""
02 — Обычный driver, но через фикстуры pytest.

Те же два теста, что и в test_01_raw_driver_no_fixtures.py: те же локаторы,
та же проверка. Отличие только в том, что поднятие и уборка сервера/браузера
вынесены в fixtures — сравните объём кода самих тестов с файлом 01.
"""

import pytest
from selenium.webdriver.common.by import By

from framework.utils.driver_factory import build_driver
from framework.utils.local_server import LocalSiteServer


@pytest.fixture(scope="module")
def site_server():
    # scope="module" — сервер поднимается один раз на все тесты этого файла,
    # а не заново для каждого, как было в 01
    server = LocalSiteServer().start()
    yield server
    server.stop()


@pytest.fixture
def driver(site_server):
    # а вот браузер — свежий для каждого теста (fixture без scope = per-test)
    drv = build_driver()
    yield drv
    # код после yield выполняется в блоке уборки pytest — даже если тест
    # ниже упадёт на assert, drv.quit() всё равно будет вызван.
    # Именно это фикстуры дают "бесплатно" по сравнению с файлом 01.
    drv.quit()


def test_successful_login(driver, site_server):
    # driver и site_server сюда подставляет pytest — сам тест их не создаёт
    driver.get(site_server.url("login.html"))

    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "login-btn")

    email_field.send_keys("test@example.com")
    password_field.send_keys("Password123")
    submit_button.click()

    welcome_message = driver.find_element(By.ID, "welcome-msg")
    assert "Test User" in welcome_message.text


def test_invalid_login_shows_error(driver, site_server):
    driver.get(site_server.url("login.html"))

    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "login-btn")

    email_field.send_keys("wrong@example.com")
    password_field.send_keys("wrongpass")
    submit_button.click()

    error_box = driver.find_element(By.ID, "login-error")
    assert "email or password" in error_box.text.lower()
