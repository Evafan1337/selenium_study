"""
09 — Загрузка файла: в <input type="file"> передаётся абсолютный путь через
send_keys(). Системное окно не открывается: WebDriver им не управляет.
"""

from pathlib import Path

from selenium.webdriver.common.by import By

from _helpers import new_driver, show_element, site_url

# заранее готовим абсолютный путь к файлу, который будем "загружать"
SAMPLE_FILE = (Path(__file__).parent / "sample_upload.txt").resolve()

# создаём драйвер
driver = new_driver()
driver.get(site_url("playground.html"))

# создаём локатор поля загрузки файла
file_input_locator = (By.ID, "file-input")
file_input = driver.find_element(*file_input_locator)
show_element(driver, file_input)
# send_keys() на <input type="file"> — это и есть "выбор файла", без диалога ОС
file_input.send_keys(str(SAMPLE_FILE))

# создаём локатор подписи с именем загруженного файла и читаем её
label_locator = (By.ID, "file-name")
label = driver.find_element(*label_locator)
show_element(driver, label)
print("Upload label after send_keys:", label.text)
assert SAMPLE_FILE.name in label.text

# закрываем браузер
driver.quit()
