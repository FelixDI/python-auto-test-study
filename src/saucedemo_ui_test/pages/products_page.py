#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-01 14:25
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : products_page.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : products page


"""实现当前页面正确访问、获取页面信息、该页面的所有按钮功能定义"""

from src.saucedemo_ui_test.common.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    ADD_TO_CART_BUTTON = "[data-test='add-to-cart-sauce-labs-backpack']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    def assert_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Products")  # BasePage封装的类方法直接用
        self.assert_url_contains("/inventory.html")

    # 页面HTML源码
    # <button data-test="add-to-cart-sauce-labs-backpack">
    #     Add to cart
    # </button>
    #
    # <button data-test="add-to-cart-sauce-labs-bike-light">
    #     Add to cart
    # </button>
    # 如果没有传参product_id，默认值"sauce-labs-backpack" 默认添加指定商品
    def add_product_to_cart(self, product_id: str = "sauce-labs-backpack"):
        self.click(f"[data-test='add-to-cart-{product_id}']")

    def get_cart_item_count(self) -> int:
        return int(self.get_text(self.CART_BADGE))

    # 高内聚低耦合：每个页面对象只负责自己的操作，不依赖其他页面
    def go_to_cart(self):
        self.click(self.CART_LINK)


# # pages/products_page.py
# from src.stage3_ui_test.common.base_page import BasePage
#
# class ProductsPage(BasePage):
#     """商品列表页面"""
#
#     # 元素定位器
#     PAGE_TITLE = ".title"
#     INVENTORY_ITEM = ".inventory_item"
#     ADD_TO_CART_BUTTON = "[data-test='add-to-cart-sauce-labs-backpack']"
#     CART_BADGE = ".shopping_cart_badge"
#     CART_LINK = ".shopping_cart_link"
#
#     def assert_page_loaded(self):
#         """断言商品页面加载成功"""
#         self.assert_text_contains(self.PAGE_TITLE, "Products")
#         self.assert_url_contains("/inventory.html")
#
#     def add_product_to_cart(self, product_id: str = "sauce-labs-backpack"):
#         """添加商品到购物车"""
#         self.click(f"[data-test='add-to-cart-{product_id}']")
#
#     def get_cart_item_count(self) -> int:
#         """获取购物车商品数量"""
#         return int(self.get_text(self.CART_BADGE))
#
#     def go_to_cart(self):
#         """进入购物车页面"""
#         self.click(self.CART_LINK)
