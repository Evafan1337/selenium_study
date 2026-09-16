"""Общие вспомогательные функции для автономных учебных примеров.

Скрипты запускаются отдельно и читаются сверху вниз как мини-уроки. Они не
зависят от pytest, но используют общую фабрику браузера проекта.
"""

import os
import sys
import time
from pathlib import Path

from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = PROJECT_ROOT / "site"

sys.path.insert(0, str(PROJECT_ROOT))  # Импорт framework работает при прямом запуске.

from framework.utils.driver_factory import build_driver  # noqa: E402

DEMO_DELAY = max(0.0, float(os.getenv("DEMO_DELAY", "1")))
HIGHLIGHT_STYLE = "outline: 4px solid #ff3b30; outline-offset: 3px; background-color: #fff3a3;"


def demo_pause(multiplier: float = 1.0) -> None:
    """Сделать паузу, чтобы учащийся успел увидеть состояние браузера."""
    if DEMO_DELAY:
        time.sleep(DEMO_DELAY * multiplier)


def highlight_element(driver, element) -> None:
    """Прокрутить страницу к элементу и временно выделить его рамкой."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});"
        "arguments[0].setAttribute('data-demo-style', arguments[0].getAttribute('style') || '');"
        "arguments[0].style.cssText += arguments[1];",
        element,
        HIGHLIGHT_STYLE,
    )


def clear_highlight(driver, element) -> None:
    try:
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[0].getAttribute('data-demo-style') || '');"
            "arguments[0].removeAttribute('data-demo-style');",
            element,
        )
    except Exception:
        pass  # После навигации или обновления DOM элемент может устареть.


def show_element(driver, element, multiplier: float = 1.0):
    """Подсветить элемент, который пример использует только для чтения."""
    highlight_element(driver, element)
    demo_pause(multiplier)
    clear_highlight(driver, element)
    return element


class _DemoListener(AbstractEventListener):
    """Показывать клики, ввод и переходы WebDriver."""

    def _before_element_action(self, element, driver) -> None:
        highlight_element(driver, element)
        demo_pause()
        clear_highlight(driver, element)

    def before_click(self, element, driver) -> None:
        self._before_element_action(element, driver)

    def after_click(self, element, driver) -> None:
        demo_pause(0.5)

    def before_change_value_of(self, element, driver) -> None:
        self._before_element_action(element, driver)

    def after_change_value_of(self, element, driver) -> None:
        demo_pause(0.5)

    def after_navigate_to(self, url, driver) -> None:
        demo_pause()

    def before_quit(self, driver) -> None:
        demo_pause()


def site_url(filename: str) -> str:
    """Вернуть file://-адрес страницы из site/ без запуска HTTP-сервера.

    Набор pytest использует локальный сервер; здесь выбран простой вариант,
    чтобы можно было сравнить оба подхода.
    """
    path, _, query = filename.partition("?")
    uri = (SITE_DIR / path).resolve().as_uri()
    return f"{uri}?{query}" if query else uri


def new_driver(headless: bool = False):
    """Создать видимый браузер, чтобы наблюдать за действиями Selenium."""
    driver = build_driver(headless=headless)
    return enable_demo(driver)


def enable_demo(driver):
    """Добавить подсветку и паузы к уже созданному WebDriver."""
    return EventFiringWebDriver(driver, _DemoListener())
