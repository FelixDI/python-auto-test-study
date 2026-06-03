#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-01 11:56
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 项目全局夹具  工具函数


"""pytest自动访问夹具,统一管理登录、商品、购物车、结账页面对象的实例，供测试文件使用，进行测试"""

import pytest

from playwright.sync_api import Page
from src.saucedemo_ui_test.pages.login_page import LoginPage
from src.saucedemo_ui_test.pages.products_page import ProductsPage
from src.saucedemo_ui_test.pages.cart_page import CartPage
from src.saucedemo_ui_test.pages.checkout_page import CheckoutPage


# pytest 会做以下事情：
# 看到login_page夹具需要一个叫page的参数
# 搜索所有已加载的插件和 conftest.py，查找有没有叫page的夹具  例如stage3_ui_test/conftest.py 实现手动创建实例page
# conftest.py没有的话，就去找到pytest-playwright插件提供的page夹具
# 运行page夹具，获取它的返回值（就是实际的浏览器页面对象）
# 把这个返回值作为参数传递给login_page夹具
# login_page夹具把这个 page 对象传递给LoginPage的构造函数
@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture(scope="function")
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture(scope="function")
def logged_in_user(page: Page, login_page: LoginPage, products_page: ProductsPage):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    products_page.assert_page_loaded()
    yield
    page.context.clear_cookies()  # 测试结束，上下文清理。pytest-playwright Fixture 每个测试都会创建新的 Browser Context


# # src/conftest.py
# import pytest
# from playwright.sync_api import Page, Browser, BrowserContext
# from src.stage3_ui_test.pages.login_page import LoginPage
# from src.stage3_ui_test.pages.products_page import ProductsPage
# from src.stage3_ui_test.pages.cart_page import CartPage
# from src.stage3_ui_test.pages.checkout_page import CheckoutPage
#
# @pytest.fixture(scope="function")
# def login_page(page: Page) -> LoginPage:
#     """登录页面夹具"""
#     return LoginPage(page)
#
# @pytest.fixture(scope="function")
# def products_page(page: Page) -> ProductsPage:
#     """商品页面夹具"""
#     return ProductsPage(page)
#
# @pytest.fixture(scope="function")
# def cart_page(page: Page) -> CartPage:
#     """购物车页面夹具"""
#     return CartPage(page)
#
# @pytest.fixture(scope="function")
# def checkout_page(page: Page) -> CheckoutPage:
#     """结账页面夹具"""
#     return CheckoutPage(page)
#
# @pytest.fixture(scope="function")
# def logged_in_user(page: Page, login_page: LoginPage, products_page: ProductsPage):
#     """已登录用户夹具：自动完成登录"""
#     login_page.navigate()
#     login_page.login("standard_user", "secret_sauce")
#     products_page.assert_page_loaded()
#     yield
#     # 测试结束后清理
#     page.context.clear_cookies()