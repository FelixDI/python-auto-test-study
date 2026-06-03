#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 16:45
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_products.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 商品页面测试


import pytest


# 执行登录 但不需要 fixture 返回值
@pytest.mark.usefixtures("logged_in_user")
def test_add_product_to_cart(products_page):
    products_page.add_product_to_cart()
    assert products_page.get_cart_item_count() == 1


@pytest.mark.usefixtures("logged_in_user")
def test_go_to_cart(products_page, cart_page):
    products_page.go_to_cart()
    cart_page.assert_page_loaded()


# # test_cases/test_products.py
# import pytest
#
# @pytest.mark.usefixtures("logged_in_user")
# def test_add_product_to_cart(products_page):
#     """测试添加商品到购物车"""
#     products_page.add_product_to_cart()
#     assert products_page.get_cart_item_count() == 1
#
# @pytest.mark.usefixtures("logged_in_user")
# def test_go_to_cart(products_page, cart_page):
#     """测试从商品页面进入购物车"""
#     products_page.go_to_cart()
#     cart_page.assert_page_loaded()