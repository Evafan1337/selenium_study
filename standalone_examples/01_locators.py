"""
01 — Стратегии поиска элементов.

Показаны все поддерживаемые Selenium стратегии By.*.
Запуск: python standalone_examples/01_locators.py
"""

from selenium.webdriver.common.by import By

from _helpers import new_driver, show_element, site_url

# создаём драйвер — открываем видимый браузер, которым будем управлять
driver = new_driver()

# открываем страницу логина — на ней есть все виды локаторов, которые хотим показать
driver.get(site_url("login.html"))

# --- By.ID — самый быстрый и однозначный вариант ---
# создаём локатор: пара (стратегия поиска, значение)
id_locator = (By.ID, "email")
# ищем элемент на странице по этому локатору
email_field = driver.find_element(*id_locator)
# подсвечиваем найденный элемент на экране, чтобы видеть, с чем работаем
show_element(driver, email_field)
print("By.ID ->", email_field.get_attribute("outerHTML")[:60])

# --- By.NAME ---
name_locator = (By.NAME, "password")
password_field = driver.find_element(*name_locator)
show_element(driver, password_field)
print("By.NAME ->", password_field.get_attribute("id"))

# --- By.CLASS_NAME ---
class_locator = (By.CLASS_NAME, "brand")
brand = driver.find_element(*class_locator)
show_element(driver, brand)
print("By.CLASS_NAME ->", brand.text)

# --- By.TAG_NAME — find_elements (с "s") возвращает список, а не один элемент ---
tag_locator = (By.TAG_NAME, "input")
all_inputs = driver.find_elements(*tag_locator)
# подсвечиваем каждый найденный элемент по очереди, но быстрее обычного
for input_element in all_inputs:
    show_element(driver, input_element, 0.35)
print("By.TAG_NAME -> found", len(all_inputs), "<input> elements")

# --- By.CSS_SELECTOR — основной способ работы с data-testid в этом проекте ---
css_locator = (By.CSS_SELECTOR, "[data-testid=login-submit]")
login_button = driver.find_element(*css_locator)
show_element(driver, login_button)
print("By.CSS_SELECTOR ->", login_button.text)

# --- By.XPATH — гибкий поиск, в том числе по видимому тексту ---
xpath_locator = (By.XPATH, "//a[contains(text(), 'Create one')]")
register_link = driver.find_element(*xpath_locator)
show_element(driver, register_link)
print("By.XPATH ->", register_link.get_attribute("href"))

# --- By.LINK_TEXT / By.PARTIAL_LINK_TEXT — поиск ссылки по её тексту ---
exact_link = driver.find_element(By.LINK_TEXT, "Create one")
partial_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Create")
show_element(driver, exact_link)
print("By.LINK_TEXT and By.PARTIAL_LINK_TEXT both resolve to:", exact_link == partial_link)

# закрываем браузер
driver.quit()
