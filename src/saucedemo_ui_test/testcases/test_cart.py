#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 16:56
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_cart.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 购物车测试


import pytest


@pytest.mark.usefixtures("logged_in_user")
def test_cart_item_count(products_page, cart_page):
    products_page.add_product_to_cart()
    products_page.go_to_cart()
    assert cart_page.get_cart_items_count() == 1


@pytest.mark.usefixtures("logged_in_user")
def test_go_to_checkout(products_page, cart_page, checkout_page):
    products_page.go_to_cart()  # 夹具中logged_in_user只进行了登录成功进入商品页面 所以要增加一步 点击购物车
    cart_page.go_to_checkout()
    checkout_page.assert_url_contains("/checkout-step-one.html")


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