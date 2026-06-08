#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-03 17:11
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_checkout.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 结算测试


import pytest


@pytest.mark.smoke
@pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
class TestCheckout:
    def test_complete_order(self, logged_in_user):
        products_page = logged_in_user
        # products_page.add_product_to_cart()
        products_page.add_product_by_index(3)
        assert products_page.get_cart_item_count() == 1

        cart_page = products_page.go_to_cart()
        cart_page.assert_cart_page_loaded()

        checkout_page = cart_page.go_to_checkout()
        checkout_page.assert_page_loaded()

        checkout_page.fill_shipping_info("Felix", "Cui", "123456")
        check_step_two_page = checkout_page.click_continue()
        check_step_two_page.assert_overview_page_loaded()

        complete_page = check_step_two_page.click_finish()
        complete_page.assert_complete_page_loaded()
        complete_page.assert_order_complete()

        products_page = complete_page.click_back_home()
        products_page.assert_page_loaded()
        assert products_page.get_cart_item_count() == 0

    def test_checkout_with_empty_info(self, logged_in_user):
        products_page = logged_in_user
        products_page.add_product_by_index(3)
        cart_page = products_page.go_to_cart()
        step_one_page = cart_page.go_to_checkout()

        step_one_page.click_continue()
        step_one_page.assert_error_message("Error: First Name is required")



# # test_cases/test_checkout.py
# import pytest
#
# @pytest.mark.smoke
# @pytest.mark.usefixtures("logged_in_user")
# def test_complete_order(products_page, cart_page, checkout_page):
#     """测试完整的下单流程"""
#     # 添加商品到购物车
#     products_page.add_product_to_cart()
#
#     # 进入购物车
#     products_page.go_to_cart()
#     cart_page.assert_page_loaded()
#
#     # 进入结账页面
#     cart_page.go_to_checkout()
#
#     # 填写收货信息
#     checkout_page.fill_shipping_info("John", "Doe", "12345")
#
#     # 完成订单
#     checkout_page.finish_order()
#
#     # 断言订单完成
#     checkout_page.assert_order_complete()