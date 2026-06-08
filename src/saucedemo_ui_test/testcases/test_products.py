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


@pytest.mark.products
@pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
class TestProductsPage:  # 共同前置条件 类式写法
    def test_page_loaded(self, logged_in_user):
        products_page = logged_in_user
        products_page.assert_page_loaded()

    def test_add_remove_product(self, logged_in_user):
        products_page = logged_in_user
        products_page.add_product_by_index(0)
        assert products_page.get_cart_item_count() == 1

        products_page.remove_product_by_index(0)
        assert products_page.get_cart_item_count() == 0

    def test_add_all_products_to_cart(self, logged_in_user):
        products_page = logged_in_user
        products_page.add_all_products_to_cart()
        assert products_page.get_cart_item_count() == 6

    def test_go_to_cart(self, logged_in_user):
        products_page = logged_in_user
        cart_page = products_page.go_to_cart()
        cart_page.assert_page_loaded()

    def test_sort_by_price_low_to_high(self, logged_in_user):
        products_page = logged_in_user
        products_page.sort_by("lohi")
        prices = products_page.get_all_prices()
        assert prices == sorted(prices), "价格从低到高排序失败"  # sorted()默认从小到大 a-z

    def test_sort_by_price_high_to_low(self, logged_in_user):
        products_page = logged_in_user
        products_page.sort_by("hilo")
        prices = products_page.get_all_prices()
        assert prices == sorted(prices, reverse=True), "价格从高到低排序失败"  # 反转

    def test_sort_by_name_a_to_z(self, logged_in_user):
        products_page = logged_in_user
        products_page.sort_by("az")

        names = products_page.get_all_product_names()
        assert names == sorted(names), "名称从A到Z排序失败"

    def test_sort_by_name_z_to_a(self, logged_in_user):
        products_page = logged_in_user
        products_page.sort_by("za")
        names = products_page.get_all_product_names()
        assert names == sorted(names, reverse=True), f"名称从Z到A排序失败"


# @pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
# def test_add_product_to_cart(logged_in_user):
#     products_page = logged_in_user
#     products_page.add_product_to_cart()
#     assert products_page.get_cart_item_count() == 1
#
#
# @pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
# def test_add_all_products_to_cart(logged_in_user):
#     products_page = logged_in_user
#     products_page.add_all_products_to_cart()
#     assert products_page.get_cart_item_count() == 6
#
#
# @pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
# def test_go_to_cart(logged_in_user):
#     products_page = logged_in_user
#     cart_page = products_page.go_to_cart()
#     cart_page.assert_page_loaded()


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