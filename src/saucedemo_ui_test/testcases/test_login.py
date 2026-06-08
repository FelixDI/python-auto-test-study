#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-01 14:28
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_login.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 登录测试  原则上测试文件test_xx.py测试用例只关心业务，不关心技术细节  利于代码维护与扩展


"""执行登录页面测试"""

import pytest
from pages.products_page import ProductsPage


@pytest.mark.smoke
@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
])  # 按用户名遍历用户数据users.json
def test_successful_login(all_users, username, login_page):
    user_data = all_users[username]

    login_page.navigate()
    login_page.login(user_data["username"], user_data["password"])

    expected_success = user_data["expected"]["login_success"]
    if expected_success:
        products_page = ProductsPage(login_page.page)
        products_page.assert_page_loaded()
    else:
        login_page.assert_text_contains(login_page.ERROR_MESSAGE, user_data["expected"]["error_message"])


def test_invalid_username(login_page):
    login_page.navigate()  # 实例调用类方法
    login_page.login("invalid_user", "secret_sauce")
    # 实例调用父类方法
    login_page.assert_text_contains(login_page.ERROR_MESSAGE, "Username and password do not match")


def test_invalid_password(login_page):
    login_page.navigate()
    login_page.login("standard_user", "wrong_password")
    login_page.assert_text_contains(login_page.ERROR_MESSAGE, "Username and password do not match")


def test_empty_credentials(login_page):
    login_page.navigate()
    login_page.login("", "")
    login_page.assert_text_contains(login_page.ERROR_MESSAGE, "Username is required")


# # test_cases/test_login.py
# import pytest
#
# @pytest.mark.smoke
# def test_successful_login(login_page, products_page):
#     """测试成功登录"""
#     login_page.navigate()
#     login_page.login("standard_user", "secret_sauce")
#     products_page.assert_page_loaded()
#
# def test_invalid_username(login_page):
#     """测试无效用户名登录"""
#     login_page.navigate()
#     login_page.login("invalid_user", "secret_sauce")
#     login_page.assert_text_contains(login_page.ERROR_MESSAGE, "Username and password do not match")
#
# def test_invalid_password(login_page):
#     """测试无效密码登录"""
#     login_page.navigate()
#     login_page.login("standard_user", "wrong_password")
#     login_page.assert_text_contains(login_page.ERROR_MESSAGE, "Username and password do not match")
#
# def test_empty_credentials(login_page):
#     """测试空凭据登录"""
#     login_page.navigate()
#     login_page.login("", "")
#     login_page.assert_text_contains(login_page.ERROR_MESSAGE, "Username is required")