from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from framework.pages.base_page import BasePage


class PlaygroundPage(BasePage):
    ALERT_BTN = (By.ID, "alert-btn")
    CONFIRM_BTN = (By.ID, "confirm-btn")
    PROMPT_BTN = (By.ID, "prompt-btn")
    DIALOG_RESULT = (By.ID, "dialog-result")

    CONTENT_FRAME = (By.ID, "content-frame")
    IFRAME_INPUT = (By.ID, "iframe-input")
    IFRAME_ECHO = (By.ID, "iframe-echo")

    DRAGGABLE = (By.ID, "draggable")
    DROPZONE = (By.ID, "dropzone")

    LOAD_BTN = (By.ID, "load-btn")
    LOADING_SPINNER = (By.ID, "loading-spinner")
    LOADED_CONTENT = (By.ID, "loaded-content")

    TOOLTIP_TRIGGER = (By.CSS_SELECTOR, "[data-testid=tooltip-trigger]")

    NEW_TAB_LINK = (By.ID, "new-tab-link")

    FILE_INPUT = (By.ID, "file-input")
    FILE_NAME = (By.ID, "file-name")

    MULTI_SELECT = (By.ID, "multi-select")
    MULTI_SELECT_RESULT = (By.ID, "multi-select-result")

    SORT_BY_NAME = (By.CSS_SELECTOR, "[data-testid=sort-by-name]")
    SORT_BY_AGE = (By.CSS_SELECTOR, "[data-testid=sort-by-age]")
    TABLE_ROWS = (By.CSS_SELECTOR, "#sortable-table-body tr")

    VOLUME_SLIDER = (By.ID, "volume-slider")
    VOLUME_VALUE = (By.ID, "volume-value")

    ENABLE_CHECKBOX = (By.ID, "enable-checkbox")
    TOGGLE_TARGET_BTN = (By.ID, "toggle-target-btn")

    def open(self, path: str = "playground.html") -> "PlaygroundPage":
        super().open(path)
        return self

    # ---- Диалоги ----
    def trigger_alert(self) -> "PlaygroundPage":
        self.click(self.ALERT_BTN)
        return self

    def trigger_confirm(self) -> "PlaygroundPage":
        self.click(self.CONFIRM_BTN)
        return self

    def trigger_prompt(self) -> "PlaygroundPage":
        self.click(self.PROMPT_BTN)
        return self

    def dialog_result_text(self) -> str:
        return self.get_text(self.DIALOG_RESULT)

    # ---- Iframe ----
    def type_into_iframe(self, text: str) -> "PlaygroundPage":
        self.switch_to_frame(self.CONTENT_FRAME)
        self.type_text(self.IFRAME_INPUT, text)
        return self

    def iframe_echo_text(self) -> str:
        text = self.get_text(self.IFRAME_ECHO)
        self.switch_to_default_content()
        return text

    # ---- Перетаскивание ----
    def drag_to_dropzone(self) -> "PlaygroundPage":
        source = self.find(self.DRAGGABLE)
        target = self.find(self.DROPZONE)
        # Синтетические движения ActionChains не всегда создают HTML5-события
        # перетаскивания, поэтому отправляем DOM-события через JavaScript.
        self.driver.execute_script(
            """
            function fireEvent(name, element, dataTransfer) {
                const event = new Event(name, {bubbles: true, cancelable: true});
                event.dataTransfer = dataTransfer;
                element.dispatchEvent(event);
            }
            const dataTransfer = new DataTransfer();
            fireEvent('dragstart', arguments[0], dataTransfer);
            fireEvent('dragover', arguments[1], dataTransfer);
            fireEvent('drop', arguments[1], dataTransfer);
            """,
            source,
            target,
        )
        return self

    def dropzone_text(self) -> str:
        return self.get_text(self.DROPZONE)

    # ---- Динамическая загрузка ----
    def click_load_and_wait(self) -> "PlaygroundPage":
        self.click(self.LOAD_BTN)
        self.wait_visible(self.LOADED_CONTENT)
        return self

    def loaded_content_text(self) -> str:
        return self.get_text(self.LOADED_CONTENT)

    # ---- Всплывающая подсказка ----
    def hover_tooltip_trigger(self) -> "PlaygroundPage":
        self.hover(self.TOOLTIP_TRIGGER)
        return self

    def tooltip_text(self) -> str:
        return self.find(self.TOOLTIP_TRIGGER).get_attribute("data-tooltip")

    # ---- Новая вкладка ----
    def open_new_tab(self) -> set[str]:
        previous_handles = set(self.driver.window_handles)
        self.click(self.NEW_TAB_LINK)
        return previous_handles

    # ---- Загрузка файла ----
    def upload_file(self, absolute_path: str) -> "PlaygroundPage":
        self.find(self.FILE_INPUT).send_keys(absolute_path)
        return self

    def uploaded_file_label(self) -> str:
        return self.get_text(self.FILE_NAME)

    # ---- Множественный выбор ----
    def select_languages(self, *labels: str) -> "PlaygroundPage":
        from selenium.webdriver.support.ui import Select

        select = Select(self.find(self.MULTI_SELECT))
        select.deselect_all()
        for label in labels:
            select.select_by_visible_text(label)
        # При программном выборе браузер не отправляет change автоматически,
        # поэтому отправляем событие самостоятельно.
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", self.find(self.MULTI_SELECT))
        return self

    def multi_select_result_text(self) -> str:
        return self.get_text(self.MULTI_SELECT_RESULT)

    # ---- Сортируемая таблица ----
    def sort_table_by_age(self) -> "PlaygroundPage":
        self.click(self.SORT_BY_AGE)
        return self

    def table_first_row_text(self) -> str:
        return self.find_all(self.TABLE_ROWS)[0].text

    # ---- Ползунок ----
    def set_volume(self, value: int) -> "PlaygroundPage":
        # <input type=range> не принимает число через send_keys — им управляют
        # только стрелки клавиатуры, по шагу за раз, поэтому "набираем" нужное
        # значение повторными нажатиями ARROW_RIGHT/ARROW_LEFT.
        slider = self.find(self.VOLUME_SLIDER)
        current = int(slider.get_attribute("value"))
        steps = value - current
        key = Keys.ARROW_RIGHT if steps > 0 else Keys.ARROW_LEFT
        for _ in range(abs(steps)):
            slider.send_keys(key)
        return self

    def volume_value(self) -> str:
        return self.get_text(self.VOLUME_VALUE)

    # ---- Включение и отключение ----
    def check_enable_checkbox(self) -> "PlaygroundPage":
        self.click(self.ENABLE_CHECKBOX)
        return self

    def is_toggle_button_enabled(self) -> bool:
        return self.find(self.TOGGLE_TARGET_BTN).is_enabled()
