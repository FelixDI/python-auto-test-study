#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 11:28
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : cart_page.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : cart page


"""cart页面访问验证、按钮功能定义"""

from src.saucedemo_ui_test.common.base_page import BasePage
from src.saucedemo_ui_test.pages.checkout_page import CheckoutPage
from src.saucedemo_ui_test.components.menu_component import MenuComponent


class CartPage(BasePage):
    PAGE_TITLE = ".title"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = "[data-test='cart-item-name']"
    REMOVE_BUTTON = "[data-test^='remove-']"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page):
        super().__init__(page)
        self.menu = MenuComponent(page)

    # 高内聚低耦合：每个页面对象只负责自己的操作，不依赖其他页面  进入cart界面 实际上是products页面的按钮功能
    # cart_page这里只需要定义一个 验证方法assert_page_loaded 被实例调用
    def assert_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Your Cart")
        self.assert_url_contains("/cart.html")

    def get_cart_item_names(self) -> str:
        items = self.page.locator(self.CART_ITEM_NAME)
        return [item.text_content() for item in items]

    def remove_item_by_index(self, index: int):
        self.page.locator(self.REMOVE_BUTTON).click()

    def get_cart_items_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def go_to_checkout(self) -> CheckoutPage:
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.page)

    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        from src.saucedemo_ui_test.pages.products_page import ProductsPage  # 避免循环导入  采用延迟导入
        return ProductsPage(self.page)


# # pages/cart_page.py
# from src.stage3_ui_test.common.base_page import BasePage
#
# class CartPage(BasePage):
#     """购物车页面"""
#
#     # 元素定位器
#     PAGE_TITLE = ".title"
#     CART_ITEM = ".cart_item"
#     CHECKOUT_BUTTON = "#checkout"
#     CONTINUE_SHOPPING_BUTTON = "#continue-shopping"
#
#     def assert_page_loaded(self):
#         """断言购物车页面加载成功"""
#         self.assert_text_contains(self.PAGE_TITLE, "Your Cart")
#         self.assert_url_contains("/cart.html")
#
#     def get_cart_items_count(self) -> int:
#         """获取购物车中商品数量"""
#         return self.page.locator(self.CART_ITEM).count()
#
#     def go_to_checkout(self):
#         """进入结账页面"""
#         self.click(self.CHECKOUT_BUTTON)





