#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 15:57
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : checkout_page.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : checkout page


from src.saucedemo_ui_test.common.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    ZIP_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    FINISH_BUTTON = "#finish"
    COMPLETE_HEADER = ".complete-header"

    def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.ZIP_CODE_INPUT, zip_code)
        self.click(self.CONTINUE_BUTTON)

    def finish_order(self):
        self.click(self.FINISH_BUTTON)

    def assert_order_complete(self):
        self.assert_text_contains(self.COMPLETE_HEADER, "Thank you for your order!")


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