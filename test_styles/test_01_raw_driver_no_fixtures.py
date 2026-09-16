"""
01 — Обычный driver, БЕЗ фикстур.

Один и тот же сценарий логина проверяется в четырёх файлах этой папки —
меняется только то, КАК устроен тест, а не то, ЧТО он проверяет. Здесь —
самый примитивный вариант: каждый тест сам поднимает сервер и браузер,
сам всё закрывает и сам ищет элементы напрямую через By.*.

Специально не убираем повторяющийся код между двумя тестами — он тут,
чтобы на следующем файле (02) было видно, что именно решают фикстуры.
"""

from selenium.webdriver.common.by import By

from framework.utils.driver_factory import build_driver
from framework.utils.local_server import LocalSiteServer


def test_successful_login():
    # поднимаем сервер сайта вручную — отдельно для каждого теста
    server = LocalSiteServer().start()
    # создаём драйвер вручную — тоже отдельно для каждого теста
    driver = build_driver()

    # открываем страницу логина по адресу локального сервера
    driver.get(server.url("login.html"))

    # создаём локаторы и находим по ним поля формы
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "login-btn")

    # заполняем форму и отправляем её
    email_field.send_keys("test@example.com")
    password_field.send_keys("Password123")
    submit_button.click()

    # после успешного логина сайт сам переходит на dashboard.html
    welcome_message = driver.find_element(By.ID, "welcome-msg")
    assert "Test User" in welcome_message.text

    # закрываем браузер и сервер вручную.
    # ВАЖНО: если бы assert выше упал, обе строки ниже НЕ выполнились бы —
    # браузер и сервер остались бы висеть в фоне. Это и есть главная причина,
    # по которой в файле 02 эта же уборка переезжает в fixture с yield.
    driver.quit()
    server.stop()


def test_invalid_login_shows_error():
    # тот же самый код поднятия окружения — скопирован один в один из теста выше
    server = LocalSiteServer().start()
    driver = build_driver()

    driver.get(server.url("login.html"))

    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "login-btn")

    email_field.send_keys("wrong@example.com")
    password_field.send_keys("wrongpass")
    submit_button.click()

    # при неверных данных сайт остаётся на той же странице и показывает блок ошибки
    error_box = driver.find_element(By.ID, "login-error")
    assert "email or password" in error_box.text.lower()

    driver.quit()
    server.stop()
