"""
Оформление: переходы по шагам, условные поля оплаты и диалог подтверждения.
"""

import allure
import pytest


@allure.epic("ShopEasy")
@allure.feature("Checkout")
class TestCheckout:

    @allure.title("Checkout with an empty cart shows a warning instead of the wizard")
    @pytest.mark.checkout
    def test_checkout_blocked_when_cart_empty(self, checkout_page):
        checkout_page.open()
        assert checkout_page.is_empty_warning_visible()

    @allure.title("Card fields are shown for card payment and hidden for cash")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_conditional_card_fields_display(self, product_page, checkout_page):
        product_page.open_by_id(2).add_to_cart()
        checkout_page.open()
        checkout_page.fill_shipping("Ada Lovelace", "1 Analytical Ave", "London", "10001")
        checkout_page.continue_to_payment()
        assert checkout_page.is_card_fields_visible()

        checkout_page.choose_payment_method("cash")
        assert not checkout_page.is_card_fields_visible()

    @allure.title("Completing all three steps and confirming places the order")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_full_checkout_flow_card_payment(self, product_page, checkout_page):
        product_page.open_by_id(1).add_to_cart()
        checkout_page.open()
        checkout_page.fill_shipping("Grace Hopper", "1 Compiler Rd", "Arlington", "22201")
        checkout_page.continue_to_payment()
        checkout_page.choose_payment_method("card")
        checkout_page.continue_to_review()
        checkout_page.place_order_and_accept()
        assert checkout_page.order_number().startswith("SE-")

    @allure.title("Dismissing the final confirm() keeps the review step active")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_dismissing_confirm_keeps_review_step(self, product_page, checkout_page):
        product_page.open_by_id(3).add_to_cart()
        checkout_page.open()
        checkout_page.fill_shipping("Alan Turing", "1 Enigma Way", "Manchester", "M1 1AA")
        checkout_page.continue_to_payment()
        checkout_page.continue_to_review()
        checkout_page.place_order_and_dismiss()
        assert checkout_page.active_step_panel_id() == "step-3"
