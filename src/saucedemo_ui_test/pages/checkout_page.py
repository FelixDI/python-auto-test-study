#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 15:57
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : checkout_page.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : checkout page

from __future__ import annotations
from src.saucedemo_ui_test.common.base_page import BasePage
from src.saucedemo_ui_test.components.menu_component import MenuComponent


class CheckoutPage(BasePage):
    PAGE_TITLE = "[data-test='title']"
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    ZIP_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page):
        super().__init__(page)  # 新增实例属性self.menu 一定要显式写父类初始化 否则父类初始化覆盖掉了，self.page不会被创建
        self.menu = MenuComponent(page)
        # BasePage 不直接持有组件；页面对象按需组合组件；组件涉及页面跳转时使用 Lazy Import（局部导入）返回目标页面对象。

    def assert_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Checkout: Your Information")
        self.assert_url_contains("/checkout-step-one.html")

    def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.ZIP_CODE_INPUT, zip_code)

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)
        step_two_page = CheckoutStepTwoPage(self.page)
        # step_two_page.assert_overview_page_loaded()  # 不按要求填写信息直接报错  这里不应该默认 断言页面已加载
        return step_two_page

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        from src.saucedemo_ui_test.pages.cart_page import CartPage
        return CartPage(self.page)

    # 不按要求填写信息，报错
    def assert_error_message(self, expected_text: str):
        self.assert_text_contains(self.ERROR_MESSAGE, expected_text)


class CheckoutStepTwoPage(BasePage):
    PAGE_TITLE = "[data-test='title']"
    FINISH_BUTTON = "#finish"
    CANCEL_BUTTON = "[data-test='cancel']"

    ITEM_TOTAL =  "[data-test='subtotal-label']"
    TAX = "[data-test='tax-label']"
    TOTAL = "[data-test='total-label']"

    def __init__(self, page):
        super().__init__(page)
        self.menu = MenuComponent(page)

    def assert_overview_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Checkout: Overview")
        self.assert_url_contains("/checkout-step-two.html")

    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        complete_page = CheckoutCompletePage(self.page)
        complete_page.assert_order_complete()
        return complete_page

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        from src.saucedemo_ui_test.pages.products_page import ProductsPage
        return ProductsPage(self.page)

    def get_item_total(self):
        text = self.get_text(self.ITEM_TOTAL)
        return float(text.replace("Item total: $", ""))

    def get_total(self):
        text = self.get_text(self.TOTAL)
        return float(text.replace("Total: $", ""))


class CheckoutCompletePage(BasePage):
    PAGE_TITLE = "[data-test='title']"
    # SUCCESS_HEADER = "[data-test=complete-header]"
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"

    def __init__(self, page):
        super().__init__(page)
        self.menu = MenuComponent(page)

    def assert_complete_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Checkout: Complete!")
        self.assert_url_contains("/checkout-complete.html")

    def assert_order_complete(self):
        self.assert_text_contains(self.COMPLETE_HEADER, "Thank you for your order!")

    def click_back_home(self):
        self.click(self.BACK_HOME_BUTTON)
        from src.saucedemo_ui_test.pages.products_page import ProductsPage
        return ProductsPage(self.page)


# 关于把常用的业务流程封装成独立的服务类
# class CheckoutService:
#     def __init__(self, products_page):
#         self.products_page = products_page
#
#     def complete_checkout(self, first_name, last_name, postal_code):
#         cart_page = self.products_page.click_cart_button()
#         checkout_page = cart_page.click_checkout()
#         checkout_page.fill_shipping_info(first_name, last_name, postal_code)
#         checkout_page.finish_order()
#         return checkout_page


# # pages/checkout_page.py
# from src.stage3_ui_test.common.base_page import BasePage
#
# class CheckoutPage(BasePage):
#     """结账页面"""
#
#     # 元素定位器
#     FIRST_NAME_INPUT = "#first-name"
#     LAST_NAME_INPUT = "#last-name"
#     ZIP_CODE_INPUT = "#postal-code"
#     CONTINUE_BUTTON = "#continue"
#     FINISH_BUTTON = "#finish"
#     COMPLETE_HEADER = ".complete-header"
#
#     def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str):
#         """填写收货信息"""
#         self.fill(self.FIRST_NAME_INPUT, first_name)
#         self.fill(self.LAST_NAME_INPUT, last_name)
#         self.fill(self.ZIP_CODE_INPUT, zip_code)
#         self.click(self.CONTINUE_BUTTON)
#
#     def finish_order(self):
#         """完成订单"""
#         self.click(self.FINISH_BUTTON)
#
#     def assert_order_complete(self):
#         """断言订单完成"""
#         self.assert_text_contains(self.COMPLETE_HEADER, "Thank you for your order!")