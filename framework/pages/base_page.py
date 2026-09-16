"""
BasePage — общая основа всех Page Object: ожидания, действия, выполнение
JavaScript, обработка диалогов и переключение окон.

Методы действий возвращают следующие Page Object, поэтому тесты читаются
как пользовательские сценарии, а не как набор низкоуровневых вызовов.
"""

from __future__ import annotations

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from framework.utils import config


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def _demo_pause(self) -> None:
        """Замедлить действия, только если задан ACTION_DELAY."""
        if config.ACTION_DELAY:
            time.sleep(config.ACTION_DELAY)

    # ---------- Навигация ----------

    def open(self, path: str = "") -> "BasePage":
        self.driver.get(self.base_url + path.lstrip("/"))
        self._demo_pause()
        return self

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    # ---------- Поиск и ожидания ----------
    #
    # Четыре разных условия ожидания существуют не для разнообразия — они
    # проверяют разные вещи, и подстановка не того часто и есть причина
    # "плавающих" тестов:
    #   find/find_all -> элемент есть в DOM (но может быть невидимым: display:none,
    #                    ещё не отрисованная модалка и т.п.)
    #   wait_visible   -> элемент есть в DOM И виден на экране
    #   wait_clickable -> виден И не задизейблен (можно кликать)
    #   wait_invisible -> дождаться, пока элемент исчезнет/скроется
    # См. standalone_examples/02_waits_explicit_vs_implicit.py для наглядной
    # демонстрации разницы между "есть в DOM" и "видим".

    def find(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: tuple[str, str]) -> list[WebElement]:
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_invisible(self, locator: tuple[str, str]) -> bool:
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_displayed(self, locator: tuple[str, str], timeout: int = 2) -> bool:
        # Это не find + .is_displayed() — тут "не появилось" не ошибка, а
        # законный результат (например, проверяем, что сообщение об ошибке
        # НЕ показалось). Поэтому ждём отдельным коротким таймаутом и гасим
        # TimeoutException, вместо того чтобы ронять тест исключением.
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    # ---------- Взаимодействия ----------

    def click(self, locator: tuple[str, str]) -> None:
        # wait_clickable, а не просто find: элемент может быть уже видимым,
        # но временно задизейбленным (например, пока форма валидируется) —
        # клик по такому элементу либо ничего не сделает, либо кинет ошибку.
        self.wait_clickable(locator).click()
        self._demo_pause()

    def type_text(self, locator: tuple[str, str], text: str, clear: bool = True) -> None:
        # clear() по умолчанию — иначе повторный вызов в том же тесте
        # дописывал бы текст к уже введённому, а не заменял его.
        field = self.wait_visible(locator)
        if clear:
            field.clear()
        field.send_keys(text)
        self._demo_pause()

    def get_text(self, locator: tuple[str, str]) -> str:
        return self.wait_visible(locator).text

    def select_by_visible_text(self, locator: tuple[str, str], text: str) -> None:
        # Select — обёртка Selenium именно над тегом <select>: обычный
        # .click() по <option> в headless-режиме работает не всегда.
        Select(self.find(locator)).select_by_visible_text(text)
        self._demo_pause()

    def select_by_value(self, locator: tuple[str, str], value: str) -> None:
        Select(self.find(locator)).select_by_value(value)
        self._demo_pause()

    def selected_options_text(self, locator: tuple[str, str]) -> list[str]:
        return [o.text for o in Select(self.find(locator)).all_selected_options]

    # ---------- Расширенные возможности Selenium ----------

    def hover(self, locator: tuple[str, str]) -> None:
        # У WebElement нет метода "навести курсор" — только ActionChains
        # умеет двигать виртуальную мышь и удерживать её над элементом,
        # чтобы сработали CSS :hover / JS mouseover.
        ActionChains(self.driver).move_to_element(self.find(locator)).perform()
        self._demo_pause()

    def scroll_into_view(self, locator: tuple[str, str]) -> None:
        # Клик может упасть с "element click intercepted", если элемент вне
        # видимой области — сначала прокручиваем к нему через JS.
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self._demo_pause()

    def js_click(self, locator: tuple[str, str]) -> None:
        # "Аварийный люк" на случай, когда обычный click() перекрыт другим
        # элементом (оверлей, sticky-хедер): JS-клик идёт мимо перехвата
        # событий мыши браузера, но и не проверяет, что элемент видим —
        # используем как исключение, а не по умолчанию.
        self.driver.execute_script("arguments[0].click();", self.find(locator))
        self._demo_pause()

    def switch_to_frame(self, locator: tuple[str, str]) -> None:
        # <iframe> — отдельный документ: пока не переключимся внутрь,
        # find() будет искать элементы iframe'а в родительском DOM и не найдёт их.
        self.driver.switch_to.frame(self.find(locator))
        self._demo_pause()

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()
        self._demo_pause()

    def accept_alert(self) -> str:
        # alert()/confirm()/prompt() — не DOM-элементы, их не найти через
        # find(); браузер блокируется, пока не позовём driver.switch_to.alert.
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        self._demo_pause()
        return text

    def dismiss_alert(self) -> str:
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.dismiss()
        self._demo_pause()
        return text

    def send_to_prompt_and_accept(self, value: str) -> None:
        alert = self.wait.until(EC.alert_is_present())
        alert.send_keys(value)
        alert.accept()
        self._demo_pause()

    def switch_to_new_window(self, previous_handles: set[str]) -> None:
        # У Selenium нет события "открылось новое окно" — сравниваем набор
        # хендлов до и после клика и забираем тот, которого раньше не было.
        new_handle = (set(self.driver.window_handles) - previous_handles).pop()
        self.driver.switch_to.window(new_handle)
        self._demo_pause()

    def switch_to_first_window(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[0])
        self._demo_pause()
