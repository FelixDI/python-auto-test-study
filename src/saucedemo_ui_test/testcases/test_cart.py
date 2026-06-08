#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 16:56
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_cart.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 购物车测试
from unittest import TestCase

import pytest


@pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
class TestCartPage:
    def test_cart_page_loaded(self, logged_in_user):
        products_page = logged_in_user
        cart_page = products_page.go_to_cart()
        cart_page.assert_cart_page_loaded()

    def test_cart_item_count(self, logged_in_user):
        products_page = logged_in_user
        products_page.add_product_to_cart()
        cart_page = products_page.go_to_cart()
        assert cart_page.get_cart_items_count() == 1

        cart_page.remove_item_by_index(0)
        assert cart_page.get_cart_items_count() == 0

    def test_go_to_checkout(self,logged_in_user):
        products_page = logged_in_user
        cart_page = products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        checkout_page.assert_url_contains("/checkout-step-one.html")

    def test_click_continue_shopping(self,logged_in_user):
        cart_page = logged_in_user.go_to_cart()
        products_page = cart_page.click_continue_shopping()
        products_page.assert_page_loaded()



# # test_cases/test_cart.py
# import pytest
#
# @pytest.mark.usefixtures("logged_in_user")
# def test_cart_item_count(products_page, cart_page):
#     """测试购物车商品数量"""
#     products_page.add_product_to_cart()
#     products_page.go_to_cart()
#     assert cart_page.get_cart_items_count() == 1
#
# @pytest.mark.usefixtures("logged_in_user")
# def test_go_to_checkout(cart_page, checkout_page):
#     """测试从购物车进入结账页面"""
#     cart_page.go_to_checkout()
#     checkout_page.assert_url_contains("/checkout-step-one.html")