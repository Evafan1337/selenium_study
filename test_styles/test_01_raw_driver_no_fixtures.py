"""
01 — Обычный driver, БЕЗ фикстур, БЕЗ хелперов проекта.

Максимально простой файл для демки: только selenium + pytest, ничего из
framework/. Браузер — видимый Chrome (headless нигде не включается), между
действиями пауза в SLEEP_SECONDS, чтобы успеть увидеть каждый шаг глазами.

Запуск:
    pytest test_styles/test_01_raw_driver_no_fixtures.py -v -s
"""

import time                         # модуль дающий функцию для ожидания
from pathlib import Path            # открытие html-верстки
                                    # (опционально)

from selenium import webdriver
from selenium.webdriver.common.by import By

# сколько секунд ждать после каждого действия — просто число, без env-переменных
SLEEP_SECONDS = 1

# страница логина открывается прямо с диска (file://...), без локального сервера
LOGIN_PAGE = (Path(__file__).resolve().parent.parent / "site" / "login.html").as_uri()

print(LOGIN_PAGE)

def test_successful_login():
    # создаём драйвер — обычный видимый Chrome, без каких-либо опций
    driver = webdriver.Chrome()

    # открываем страницу логина
    driver.get(LOGIN_PAGE)
    time.sleep(SLEEP_SECONDS)

    # создаём локаторы и находим по ним поля формы
    # сохраняем их в переменную
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "login-btn")

    # заполняем форму — с паузой после каждого поля, чтобы видеть ввод
    email_field.send_keys("test@example.com")
    time.sleep(SLEEP_SECONDS)
    password_field.send_keys("Password123")
    time.sleep(SLEEP_SECONDS)

    # отправляем форму
    submit_button.click()
    time.sleep(SLEEP_SECONDS)

    # после успешного логина сайт сам переходит на dashboard.html
    welcome_message = driver.find_element(By.ID, "welcome-msg")
    assert "Test User" in welcome_message.text
    time.sleep(SLEEP_SECONDS)

    # закрываем браузер вручную.
    # ВАЖНО: если бы assert выше упал, эта строка НЕ выполнилась бы —
    # браузер остался бы висеть в фоне. Это и есть главная причина, по
    # которой в файле 02 закрытие переезжает в fixture с yield.
    driver.quit()


def test_invalid_login_shows_error():
    # тот же самый код поднятия окружения — скопирован один в один из теста выше
    driver = webdriver.Chrome()

    driver.get(LOGIN_PAGE)
    time.sleep(SLEEP_SECONDS)

    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "login-btn")

    email_field.send_keys("wrong@example.com")
    time.sleep(SLEEP_SECONDS)
    password_field.send_keys("wrongpass")
    time.sleep(SLEEP_SECONDS)
    submit_button.click()
    time.sleep(SLEEP_SECONDS)

    # при неверных данных сайт остаётся на той же странице и показывает блок ошибки
    error_box = driver.find_element(By.ID, "login-error")
    assert "email or password" in error_box.text.lower()
    time.sleep(SLEEP_SECONDS)

    driver.quit()
