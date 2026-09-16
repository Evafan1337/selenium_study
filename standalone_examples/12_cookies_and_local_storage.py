"""
12 — Cookies и localStorage.

Пример показывает оба хранилища и прямую подготовку авторизованного состояния.
Для cookie нужен HTTP-адрес, поэтому сайт запускается на локальном сервере.
"""

import json

from _helpers import new_driver, show_element
from framework.utils.local_server import LocalSiteServer

# поднимаем локальный сервер для site/ — cookie требуют настоящего http://-адреса
server = LocalSiteServer().start()
# создаём драйвер
driver = new_driver()
driver.get(server.url("index.html"))

# ---------- Cookies: нативный API WebDriver ----------
driver.add_cookie({"name": "demo_cookie", "value": "abc123"})
print("Cookie set:", driver.get_cookie("demo_cookie"))
driver.delete_cookie("demo_cookie")
print("Cookie after delete:", driver.get_cookie("demo_cookie"))

# ---------- localStorage: своего API у WebDriver нет, работаем через JS ----------
driver.execute_script(
    "localStorage.setItem('shopeasy_auth', arguments[0]);",
    json.dumps({"email": "test@example.com", "name": "Test User"}),
)
auth_raw = driver.execute_script("return localStorage.getItem('shopeasy_auth');")
print("localStorage auth (seeded without touching the login form):", auth_raw)

# ---------- Переходим в кабинет — он увидит уже подготовленную авторизацию ----------
driver.get(server.url("dashboard.html"))
welcome_locator = ("id", "welcome-msg")
welcome = driver.find_element(*welcome_locator)
show_element(driver, welcome)
print("Dashboard welcome message after seeding auth via JS:", welcome.text)

# закрываем браузер и останавливаем локальный сервер
driver.quit()
server.stop()
