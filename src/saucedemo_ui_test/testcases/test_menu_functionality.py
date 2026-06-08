#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-04 14:55
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_menu_functionality.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 菜单组件测试


import pytest


@pytest.mark.menu
@pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
class TestMenuFunctionality:  # 测试用例共同前置条件fixture: logged_in_user 用类式写法
    def test_menu_open_close(self, logged_in_user):
        products_page = logged_in_user
        menu = products_page.menu
        menu.open()
        menu.assert_menu_items_visible()

        menu.close()
        assert not menu.is_open

    def test_logout_from_products_page(self, login_page, logged_in_user):
        products_page = logged_in_user
        products_page.menu.click_logout()

        login_page.assert_element_visible(login_page.LOGIN_BUTTON)

    def test_reset_app_state(self, logged_in_user):
        products_page = logged_in_user

        products_page.add_product_by_index(0)
        assert products_page.get_cart_item_count() == 1

        products_page.menu.click_reset_app_state()
        assert products_page.get_cart_item_count() == 0  # 购物车为空时 没有角标 针对报错重写get_cart_item_count()

    # 明确组件功能只需要选一个页面测试即可，不需要每个页面都测一次
    def test_navigate_from_cart_page(self, logged_in_user):
        products_page = logged_in_user
        cart_page = products_page.go_to_cart()

        products_page = cart_page.menu.click_all_items()
        products_page.assert_page_loaded()


# # 测试用例示例：test_menu_functionality.py
# import pytest
#
# @pytest.mark.menu
# @pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
# class TestMenuFunctionality:
#     """测试侧边栏菜单的所有功能"""
#
#     def test_menu_open_close(self, logged_in_user):
#         """测试菜单的打开和关闭"""
#         products_page = logged_in_user
#
#         # 打开菜单
#         products_page.menu.open()
#         products_page.menu.assert_menu_items_visible()
#
#         # 关闭菜单
#         products_page.menu.close()
#         assert not products_page.menu.is_open
#
#     def test_logout_from_products_page(self, logged_in_user):
#         """测试从商品列表页退出登录"""
#         products_page = logged_in_user
#
#         # 链式调用：点击退出登录，返回登录页
#         login_page = products_page.menu.click_logout()
#
#         # 断言成功跳转到登录页
#         login_page.assert_visible(login_page.LOGIN_BUTTON)
#
#     def test_reset_app_state(self, logged_in_user):
#         """测试重置应用状态"""
#         products_page = logged_in_user
#
#         # 添加商品到购物车
#         products_page.add_product_by_index(0)
#         assert products_page.get_cart_item_count() == 1
#
#         # 重置应用状态
#         products_page.menu.click_reset_app_state()
#
#         # 断言购物车已清空
#         assert products_page.get_cart_item_count() == 0
#
#     def test_navigate_from_cart_page(self, logged_in_user):
#         """测试从购物车页面通过菜单导航"""
#         products_page = logged_in_user
#         cart_page = products_page.click_cart_button()
#
#         # 从购物车页面点击"所有商品"返回商品列表
#         products_page = cart_page.menu.click_all_items()
#         products_page.assert_page_loaded()