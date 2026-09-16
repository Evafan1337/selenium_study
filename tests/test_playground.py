"""
Полигон: диалоги, iframe, перетаскивание, динамические ожидания,
множественный выбор, сортируемые таблицы и включение элементов.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Playground")
class TestPlayground:

    @allure.title("alert() can be accepted and its outcome observed")
    @pytest.mark.smoke
    @pytest.mark.playground
    def test_alert_accept(self, playground_page):
        playground_page.open()
        playground_page.trigger_alert()
        playground_page.accept_alert()
        assert "dismissed" in playground_page.dialog_result_text()

    @allure.title("confirm() can be dismissed")
    @pytest.mark.playground
    def test_confirm_dismiss(self, playground_page):
        playground_page.open()
        playground_page.trigger_confirm()
        playground_page.dismiss_alert()
        assert "dismissed" in playground_page.dialog_result_text()

    @allure.title("prompt() accepts typed input and the page echoes it back")
    @pytest.mark.playground
    def test_prompt_send_keys(self, playground_page):
        playground_page.open()
        playground_page.trigger_prompt()
        playground_page.send_to_prompt_and_accept("Ada")
        assert "Ada" in playground_page.dialog_result_text()

    @allure.title("Typing inside an iframe is isolated until you switch back out")
    @pytest.mark.smoke
    @pytest.mark.playground
    def test_iframe_interaction(self, playground_page):
        playground_page.open()
        playground_page.type_into_iframe("hello from selenium")
        assert playground_page.iframe_echo_text() == "hello from selenium"

    @allure.title("Dragging an element into the dropzone updates its label")
    @pytest.mark.playground
    def test_drag_and_drop(self, playground_page):
        playground_page.open()
        playground_page.drag_to_dropzone()
        assert playground_page.dropzone_text() == "Dropped!"

    @allure.title("Dynamically loaded content appears after an explicit wait")
    @pytest.mark.smoke
    @pytest.mark.playground
    def test_dynamic_loading_wait(self, playground_page):
        playground_page.open()
        playground_page.click_load_and_wait()
        assert "dynamically loaded" in playground_page.loaded_content_text()

    @allure.title("A hover-only tooltip exposes its text via the data attribute")
    @pytest.mark.playground
    def test_hover_tooltip(self, playground_page):
        playground_page.open()
        playground_page.hover_tooltip_trigger()
        assert playground_page.tooltip_text() == "I appear on hover"

    @allure.title("Opening a link with target=_blank can be followed by switching window handles")
    @pytest.mark.playground
    def test_new_tab_window_switch(self, playground_page):
        playground_page.open()
        previous_handles = playground_page.open_new_tab()
        playground_page.switch_to_new_window(previous_handles)
        assert "new_tab.html" in playground_page.current_url
        playground_page.driver.close()
        playground_page.switch_to_first_window()

    @allure.title("Selecting multiple options in a multi-select reports all of them")
    @pytest.mark.playground
    def test_multi_select_dropdown(self, playground_page):
        playground_page.open()
        playground_page.select_languages("Python", "Go")
        result = playground_page.multi_select_result_text()
        assert "Python" in result and "Go" in result

    @allure.title("Sorting the table by age reorders the rows")
    @pytest.mark.playground
    def test_sortable_table(self, playground_page):
        playground_page.open()
        assert playground_page.table_first_row_text().startswith("Charlie")
        playground_page.sort_table_by_age()
        assert playground_page.table_first_row_text().startswith("Alice")

    @allure.title("Arrow-key presses move the range slider to an exact value")
    @pytest.mark.playground
    def test_volume_slider(self, playground_page):
        playground_page.open()
        playground_page.set_volume(80)
        assert playground_page.volume_value() == "80"

    @allure.title("A checkbox can enable an initially disabled button")
    @pytest.mark.playground
    def test_enable_disabled_button(self, playground_page):
        playground_page.open()
        assert not playground_page.is_toggle_button_enabled()
        playground_page.check_enable_checkbox()
        assert playground_page.is_toggle_button_enabled()
