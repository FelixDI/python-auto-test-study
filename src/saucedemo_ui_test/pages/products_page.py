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
from src.saucedemo_ui_test.components.menu_component import MenuComponent


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
    ADD_TO_CART_BUTTONS = "[data-test^='add-to-cart-']"  # ^=表示以某个字符串开头（starts with） 前缀
    REMOVE_BUTTON = "[data-test^='remove-']"
    SORT_CONTAINER = "[data-test='product-sort-container']"

    def __init__(self, page):
        super().__init__(page)
        self.menu = MenuComponent(self.page)  # 注入菜单组件

    def assert_page_loaded(self):
        self.assert_text_contains(self.PAGE_TITLE, "Products")  # BasePage封装的类方法直接用
        self.assert_url_contains("/inventory.html")

    # <img src="img1.jpg">
    # <img src="img2.jpg">
    # <img src="img3.jpg">
    def get_all_product_images(self) -> list[str]:
        images = self.page.locator(self.PRODUCT_IMAGE)
        # return [image.get_attribute("src") for image in images]
        return [images.nth(i).get_attribute("src") for i in range(images.count())]

    # <div data-test="inventory-item">
    #     <a data-test="inventory-item-name">Sauce Labs Backpack</a>
    # </div>
    #
    # <div data-test="inventory-item">
    #     <a data-test="inventory-item-name">Sauce Labs Bike Light</a>
    # </div>
    #
    # <div data-test="inventory-item">
    #     <a data-test="inventory-item-name">Sauce Labs Bolt T-Shirt</a>
    # </div>
    #
    # ...
    # Playwright 的 Locator 默认就是“匹配结果集合”，一个定位器可以同时匹配 1 个、6 个、100 个元素，不需要为每个商品单独写定位器。
    def get_product_name_by_index(self, index: int) ->str:
        return self.page.locator(self.PRODUCT_NAME).nth(index).text_content

    # 用于名称排序
    def get_all_product_names(self) -> list[str]:
        return self.page.locator(self.PRODUCT_NAME).all_text_contents()

    def add_product_by_index(self, index: int):
        """添加指定索引的商品到购物车"""
        self.page.locator(self.ADD_TO_CART_BUTTONS).nth(index).click()  # nth(0～5)

    # button Locator 集合是动态的，点击后 add-to-cart 按钮会变成 remove 按钮，导致集合长度变化，nth(i) 后面的索引失效，所以超时
    def add_all_products_to_cart(self):
        # buttons = self.page.locator(self.ADD_TO_CART_BUTTONS)  # locator对象 6个商品按钮组成的 Locator 集合
        # count = buttons.count()

        # for _ in range(count):
        #     buttons.first.click()

        # 为了统一风格.nth 直接遍历商品卡片
        items = self.page.locator(self.INVENTORY_ITEM)

        for i in range(items.count()):
            items.nth(i).locator("button").click()



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

    def remove_product_by_index(self, index: int):
        self.page.locator(self.REMOVE_BUTTON).nth(index).click()

    # def get_cart_item_count(self) -> int:
        # return int(self.get_text(self.CART_BADGE))
    def get_cart_item_count(self) -> int:
        if not self.page.locator(self.CART_BADGE).is_visible():  # 购物车为空时 不显示角标0 所以这里用return返回0
            return 0

        return int(self.get_text(self.CART_BADGE))

    def sort_by(self, value: str):
        self.page.locator(self.SORT_CONTAINER).select_option(value)
        selected_value = self.page.locator(self.SORT_CONTAINER).input_value()
        assert selected_value == value, f"排序失败，预期选中{value}，实际选中{selected_value}"

    # 用于价格排序
    def get_all_prices(self) -> list[float]:
        price_elements = self.page.locator(self.PRODUCT_PRICE)
        prices = []
        for price_text in price_elements.all_text_contents():
            clean_price = price_text.strip().replace("$", "")
            prices.append(float(clean_price))

        return prices

    def go_to_cart(self) -> CartPage:
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
