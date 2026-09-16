# Standalone-примеры

Каждый скрипт здесь демонстрирует ровно одну возможность Selenium,
полностью самодостаточен (сам открывает браузер, делает своё дело,
закрывает его) и рассчитан на чтение сверху вниз как мини-туториал —
это не часть pytest-набора из `tests/`.

Запускать любой из них можно прямо из корня проекта:

```bash
python standalone_examples/01_locators.py
```

По умолчанию они открывают **видимый** браузер (в отличие от pytest-набора,
который по умолчанию headless), подсвечивают активные элементы красной рамкой
и делают паузу в 1 секунду. Скорость демонстрации настраивается переменной:

```bash
DEMO_DELAY=2 python standalone_examples/05_alerts_and_popups.py
DEMO_DELAY=0.3 python standalone_examples/08_select_dropdowns.py
```

| Скрипт | Тема |
|---|---|
| `01_locators.py` | Все стратегии локаторов `By.*` |
| `02_waits_explicit_vs_implicit.py` | Почему явный `WebDriverWait` надёжнее неявных ожиданий для динамического контента |
| `03_action_chains.py` | Наведение курсора, управление ползунком с клавиатуры, click-and-hold |
| `04_drag_and_drop.py` | HTML5 drag-and-drop и почему `ActionChains.drag_and_drop` часто не срабатывает |
| `05_alerts_and_popups.py` | `alert()`, `confirm()`, `prompt()` |
| `06_iframes.py` | Переключение в `<iframe>` и обратно |
| `07_windows_and_tabs.py` | Работа с несколькими окнами (window handles) |
| `08_select_dropdowns.py` | Хелпер `Select` для одиночного/множественного выбора |
| `09_file_upload.py` | Загрузка файла через `send_keys()` |
| `10_screenshots.py` | Скриншот всей страницы, отдельного элемента и в base64 |
| `11_javascript_executor.py` | `execute_script()` для чтения/записи состояния страницы |
| `12_cookies_and_local_storage.py` | Cookie API против localStorage через JS |
| `13_browser_options.py` | Headless-режим и другие опции Chrome |

`_helpers.py` — общая служебная логика (не пронумерованный пример): создаёт
драйвер и превращает относительные пути в `file://`-адреса внутри папки `site/`.
