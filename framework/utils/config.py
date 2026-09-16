"""
Общие настройки запуска из переменных окружения. CI может менять поведение,
не редактируя исходный код.

    HEADLESS=true|false    -> запуск без окна (по умолчанию true)
    BROWSER=chrome|firefox -> выбор браузера (по умолчанию chrome)
    EXPLICIT_WAIT=10       -> таймаут явного ожидания в секундах
    ACTION_DELAY=0         -> пауза после действий для демонстрации

Нет настройки implicit wait — и это осознанно: весь framework/ построен на
явных ожиданиях (BasePage.wait_*), а смешивать implicit и explicit wait в
одном драйвере — известный антипаттерн Selenium (см. стандартный пример
standalone_examples/02_waits_explicit_vs_implicit.py). driver_factory.py
поэтому implicitly_wait() не вызывает вовсе.
"""

import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


HEADLESS: bool = _env_bool("HEADLESS", True)
BROWSER: str = os.getenv("BROWSER", "chrome").lower()
EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))
ACTION_DELAY: float = max(0.0, float(os.getenv("ACTION_DELAY", "0")))
