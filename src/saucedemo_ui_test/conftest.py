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
import json
import os
import allure

from playwright.sync_api import Page
from src.saucedemo_ui_test.pages.login_page import LoginPage
from src.saucedemo_ui_test.pages.products_page import ProductsPage


# 整个测试会话只执行一次 加载所有用户数据
@pytest.fixture(scope="session")
def all_users():
    data_file = os.path.join(str(os.path.dirname(__file__)), "data", "users.json")
    # 拼接路径/Users/felix/project/data/users.json  或者推荐用from pathlib import Path
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f) # dict  返回 JSON 对应的 Python 对象  json格式决定 {} -> dict   [] -> list


# pytest 会做以下事情：
# 看到login_page夹具需要一个叫page的参数
# 搜索所有已加载的插件和 conftest.py，查找有没有叫page的夹具  例如conftest.py 实现手动创建实例page
# conftest.py没有的话，就去找到pytest-playwright插件提供的page夹具
# 运行page夹具，获取它的返回值（就是实际的浏览器页面对象）
# 把这个返回值作为参数传递给login_page夹具
# login_page夹具把这个 page实例 传递给LoginPage的构造函数（继承父类BasePage）
@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

# 除 login_page之外 后续页面都涉及业务链路 fixture不宜直接提供
# @pytest.fixture(scope="function")
# def products_page(page: Page) -> ProductsPage:
#     return ProductsPage(page)
#
#
# @pytest.fixture(scope="function")
# def cart_page(page: Page) -> CartPage:
#     return CartPage(page)
#
#
# @pytest.fixture(scope="function")
# def checkout_page(page: Page) -> CheckoutPage:
#     return CheckoutPage(page)

#
# @pytest.fixture(scope="function")
# def logged_in_user(page: Page, login_page: LoginPage, products_page: ProductsPage):
#     login_page.navigate()
#     login_page.login("standard_user", "secret_sauce")
#     products_page.assert_page_loaded()
#     yield
    # page.context.clear_cookies()  # 测试结束，上下文清理。pytest-playwright Fixture 每个测试都会创建新的 Browser Context


# 作为6种用户测试的接口  暂时不深入另外五种用户的测试用例
#     "locked_out_user",
#     "problem_user",
#     "performance_glitch_user",
#     "error_user",
#     "visual_user"
@pytest.fixture(scope="function")
def logged_in_user(request, login_page, all_users):
    # @pytest.mark.parametrize("logged_in_user", ["standard_user"], indirect=True)
    username = request.param  # request是Pytest的内置Fixture,它包含当前测试上下文信息。 request.param=="standard_user"
    user_data = all_users[username]
    # 传参login_page 浏览器about:blank, login_page.navigate() -> login_page, login_page.login() -> products_page
    login_page.navigate()
    # 若logged_in_user传参fixture创建的products_page,提前引入了 products_page 这个“语义对象”，但页面状态还没到 products
    login_page.login(user_data["username"], user_data["password"])  # login → products
    # users.json中的locked_out_user被排除
    if user_data["expected"]["login_success"]:
        products_page = ProductsPage(login_page.page)
        products_page.assert_page_loaded()
        yield products_page
    else:
        yield login_page


# 失败自动截图钩子
# pytest_runtest_makereport(item,call)是 pytest 官方预定义好的Hook函数签名 不能更改
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_user")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name=f"失败截图-{item.name}",
                attachment_type=allure.attachment_type.PNG
            )


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



# import pytest
# import json
# import os
#
# from playwright.sync_api import Page
#
# from src.saucedemo_ui_test.pages.login_page import LoginPage
# from src.saucedemo_ui_test.pages.products_page import ProductsPage
#
#
# # =========================
# # 1. 基础数据 Fixture
# # =========================
# @pytest.fixture(scope="session")
# def all_users():
#     data_file = os.path.join(
#         os.path.dirname(__file__),
#         "data",
#         "users.json"
#     )
#     with open(data_file, "r", encoding="utf-8") as f:
#         return json.load(f)
#
#
# # =========================
# # 2. Playwright 提供的 page（来自 pytest-playwright）
# # =========================
# @pytest.fixture(scope="function")
# def base_page(page: Page):
#     """
#     统一入口：所有 Page Object 都基于同一个 page
#     """
#     return page
#
#
# # =========================
# # 3. Page Object：登录页
# # =========================
# @pytest.fixture(scope="function")
# def login_page(base_page):
#     return LoginPage(base_page)
#
#
# # =========================
# # 4. 登录状态（核心fixture）
# #    👉 推荐只保留这个“业务态fixture”
# # =========================
# @pytest.fixture(scope="function")
# def logged_in_user(request, login_page, all_users):
#     username = request.param
#     user_data = all_users[username]
#
#     login_page.navigate()
#
#     login_page.login(
#         user_data["username"],
#         user_data["password"]
#     )
#
#     # 登录成功后直接构建 products_page
#     products_page = ProductsPage(login_page.page)
#     products_page.assert_page_loaded()
#
#     yield products_page
#
#
# # =========================
# # 5. 可选：关闭自动截图（如果你有hook）
# # =========================
# @pytest.fixture(scope="function", autouse=False)
# def debug_mode():
#     return False