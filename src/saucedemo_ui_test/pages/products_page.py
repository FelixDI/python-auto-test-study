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
from src.saucedemo_ui_test.pages.cart_page import CartPage


class ProductsPage(BasePage):
    PAGE_TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    # INVENTORY_ITEM = "[data-test='inventory-item']"
    # ADD_TO_CART_BUTTON = "[data-test='add-to-cart-sauce-labs-backpack']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    # ADD_TO_CART_BUTTON = "[data-test='add-to-cart-{product_id}']"
    PRODUCT_IMAGE = "[data-test='inventory-item-img']"
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    ADD_TO_CART_BUTTONS = "[data-test^='add-to-cart-']"  # ^=表示以某个字符串开头（starts with）
    REMOVE_BUTTON = "[data-test^='remove-']"
    SORT_CONTAINER = "[data-test='product-sort-container']"

    # def __init__(self, page):
    #     super().__init__(page)
    #     self.menu = MenuComponent(self.page)  # 注入菜单组件

    def assert_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Products")  # BasePage封装的类方法直接用
        self.assert_url_contains("/inventory.html")

    def add_product_by_index(self, index: int):
        """添加指定索引的商品到购物车"""
        self.page.locator(self.ADD_TO_CART_BUTTONS).nth(index).click()

    def add_all_products_to_cart(self):
        buttons = self.page.locator(self.ADD_TO_CART_BUTTONS)  # locator对象 6个按钮组成的 Locator 集合
        count = buttons.count()

        for _ in range(count):
            buttons.first.click()

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

    # def get_cart_item_count(self) -> int:
        # return int(self.get_text(self.CART_BADGE))
    def get_cart_item_count(self) -> int:
        if not self.page.locator(self.CART_BADGE).is_visible():  # 购物车为空时 不显示角标0 所以这里用return返回0
            return 0

        return int(self.get_text(self.CART_BADGE))

    # 高内聚低耦合：每个页面对象只负责自己的操作，不依赖其他页面
    def go_to_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.page)


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
