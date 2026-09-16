"""
05 — Диалоги JavaScript: alert(), confirm() и prompt().

Нативный диалог нельзя найти через find_element: сначала нужно переключиться
на него с помощью driver.switch_to.alert.
"""

from selenium.webdriver.common.by import By

from _helpers import new_driver, show_element, site_url

# создаём драйвер
driver = new_driver()
driver.get(site_url("playground.html"))

# ---------- alert() — доступно только подтверждение, кнопки отмены нет ----------
# создаём локатор кнопки, которая вызывает alert()
alert_btn_locator = (By.ID, "alert-btn")
driver.find_element(*alert_btn_locator).click()
# диалог — не элемент DOM, его не найти через find_element; переключаемся на него отдельно
alert = driver.switch_to.alert
print("alert() text:", alert.text)
alert.accept()

# ---------- confirm() — accept() нажимает OK, dismiss() — «Отмена» ----------
confirm_btn_locator = (By.ID, "confirm-btn")
result_locator = (By.ID, "dialog-result")

driver.find_element(*confirm_btn_locator).click()
driver.switch_to.alert.dismiss()
result_after_dismiss = driver.find_element(*result_locator)
show_element(driver, result_after_dismiss)
print("Result after dismissing confirm():", result_after_dismiss.text)

driver.find_element(*confirm_btn_locator).click()
driver.switch_to.alert.accept()
result_after_accept = driver.find_element(*result_locator)
show_element(driver, result_after_accept)
print("Result after accepting confirm():", result_after_accept.text)

# ---------- prompt() — send_keys() вводит текст перед подтверждением ----------
prompt_btn_locator = (By.ID, "prompt-btn")
driver.find_element(*prompt_btn_locator).click()
prompt = driver.switch_to.alert
prompt.send_keys("Grace Hopper")
prompt.accept()
result_after_prompt = driver.find_element(*result_locator)
show_element(driver, result_after_prompt)
print("Result after prompt():", result_after_prompt.text)

# закрываем браузер
driver.quit()
