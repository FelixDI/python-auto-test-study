#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-04 09:54
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : menu_component.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : POM 进阶到组件化设计component object的标准实践。侧边栏菜单是所有登录后页面都共享的公共组件，所有页面复用避免重复代码。


from playwright.sync_api import expect
from src.saucedemo_ui_test.common.base_page import BasePage


class MenuComponent(BasePage):
    # 全部使用官方data-test属性，最稳定
    MENU_BUTTON = "#react-burger-menu-btn"
    # MENU_CLOSE_BUTTON = "[data-test='close-menu']"
    MENU_CLOSE_BUTTON = "#react-burger-cross-btn"
    # MENU_OVERLAY = ".bm-overlay"
    ALL_ITEMS_LINK = "[data-test='inventory-sidebar-link']"
    ABOUT_LINK = "[data-test='about-sidebar-link']"
    LOGOUT_LINK = "[data-test='logout-sidebar-link']"
    RESET_APP_STATE_LINK = "[data-test='reset-sidebar-link']"

    def __init__(self, page):
        super().__init__(page)
        self.is_open = False

    def open(self):
        if not self.is_open:
            self.click(self.MENU_BUTTON)
            self.assert_element_visible(self.MENU_CLOSE_BUTTON)
            self.is_open = True

    def close(self):
        if self.is_open:
            self.click(self.MENU_CLOSE_BUTTON)
            expect(self.page.locator(self.ALL_ITEMS_LINK)).not_to_be_visible()
            self.is_open = False

    def assert_menu_items_visible(self):
        self.open()
        self.assert_element_visible(self.ALL_ITEMS_LINK)
        self.assert_element_visible(self.ABOUT_LINK)
        self.assert_element_visible(self.LOGOUT_LINK)
        self.assert_element_visible(self.RESET_APP_STATE_LINK)

    # def click_all_items(self, products_page_class):  # 外部传入class 避免循环导入
    def click_all_items(self):
        self.open()
        self.click(self.ALL_ITEMS_LINK)
        self.is_open = False  # 实际上在products_page页面时 点击all items 菜单不关闭 与其他页面功能不一致
        from src.saucedemo_ui_test.pages.products_page import ProductsPage  # 解决循环导入 采用延迟导入统一风格
        return ProductsPage(self.page)
        # return products_page_class(self.page)

    # 测试文件
    # from src.saucedemo_ui_test.pages.products_page import ProductsPage
    #
    #
    # def test_menu_all_items(logged_in_user):
    #
    #     products_page = logged_in_user
    #
    #     new_page = products_page.menu.click_all_items(
    #         ProductsPage
    #     )
    #
    #     new_page.assert_page_loaded()

    def click_about(self):
        self.open()
        self.click(self.ABOUT_LINK)
        self.page.wait_for_url("https://saucelabs.com")
        self.is_open = False

    def click_logout(self):
        self.open()
        self.click(self.LOGOUT_LINK)
        self.is_open = False

    def click_reset_app_state(self):
        self.open()
        self.click(self.RESET_APP_STATE_LINK)
        self.close()  # 手动关闭


# # src/stage3_ui_test/components/menu_component.py
# from src.stage3_ui_test.common.base_page import BasePage
# from src.stage3_ui_test.pages.login_page import LoginPage
# from src.stage3_ui_test.pages.products_page import ProductsPage
#
# class MenuComponent(BasePage):
#     """侧边栏菜单组件：所有登录后页面共享"""
#
#     # 全部使用官方data-test属性，最稳定
#     MENU_BUTTON = "[data-test='open-menu']"
#     MENU_CLOSE_BUTTON = "[data-test='close-menu']"
#     ALL_ITEMS_LINK = "[data-test='inventory-sidebar-link']"
#     ABOUT_LINK = "[data-test='about-sidebar-link']"
#     LOGOUT_LINK = "[data-test='logout-sidebar-link']"
#     RESET_APP_STATE_LINK = "[data-test='reset-sidebar-link']"
#
#     def __init__(self, page):
#         super().__init__(page)
#         self.is_open = False  # 菜单状态标记
#
#     def open(self):
#         """打开侧边栏菜单"""
#         if not self.is_open:
#             self.click(self.MENU_BUTTON)
#             # 完全使用你BasePage里的方法名
#             self.assert_element_visible(self.MENU_CLOSE_BUTTON)
#             self.is_open = True
#             print("✓ 侧边栏菜单已打开")
#
#     def close(self):
#         """关闭侧边栏菜单"""
#         if self.is_open:
#             self.click(self.MENU_CLOSE_BUTTON)
#             # 用你已有的is_visible方法实现不可见断言
#             assert not self.is_visible(self.MENU_CLOSE_BUTTON), "菜单关闭失败"
#             self.is_open = False
#             print("✓ 侧边栏菜单已关闭")
#
#     def click_all_items(self) -> ProductsPage:
#         """点击"所有商品"，返回商品列表页"""
#         self.open()
#         self.click(self.ALL_ITEMS_LINK)
#         products_page = ProductsPage(self.page)
#         products_page.assert_page_loaded()
#         self.is_open = False
#         return products_page
#
#     def click_logout(self) -> LoginPage:
#         """点击"退出登录"，返回登录页"""
#         self.open()
#         self.click(self.LOGOUT_LINK)
#         login_page = LoginPage(self.page)
#         # 用你BasePage里的assert_element_visible
#         self.assert_element_visible(login_page.LOGIN_BUTTON)
#         self.is_open = False
#         print("✓ 已成功退出登录")
#         return login_page
#
#     def click_reset_app_state(self):
#         """点击"重置应用状态"，清空购物车"""
#         self.open()
#         self.click(self.RESET_APP_STATE_LINK)
#         self.close()
#         print("✓ 应用状态已重置，购物车已清空")
#
#     def assert_menu_items_visible(self):
#         """断言所有菜单项都可见"""
#         self.open()
#         self.assert_element_visible(self.ALL_ITEMS_LINK)
#         self.assert_element_visible(self.ABOUT_LINK)
#         self.assert_element_visible(self.LOGOUT_LINK)
#         self.assert_element_visible(self.RESET_APP_STATE_LINK)
#         print("✓ 所有菜单项都可见")