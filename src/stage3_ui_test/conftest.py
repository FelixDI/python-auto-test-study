#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-28 14:30
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : UI测试夹具 自动浏览器页面登录

import pytest
from playwright.sync_api import sync_playwright,Page
import allure

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser

        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()   # 浏览器上下文 一个浏览器进程里，模拟多个互相隔离的真实用户 同时测试
    page = context.new_page()
    yield page

    context.close()

@pytest.fixture
def logged_in_page(page):
    page.goto("https://www.saucedemo.com")
    page.locator("[placeholder='Username']").fill("standard_user")
    page.locator("[placeholder='Password']").fill("secret_sauce")
    page.locator("#login-button").click()
# .title 是 SauceDemo 商品页面标题“Products”的 CSS 类名。这个显式等待能确保后续操作（比如断言商品数量）在正确的页面上执行。
    page.wait_for_selector(".title")
    return page


@pytest.hookimpl(tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport(item,call):  # pytest_runtest_makereport(item,call)是 pytest 官方预定义好的Hook签名
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page:
            screenshot = page.screenshot()

            allure.attach(
                screenshot,
                name = f"失败截图-{item.name}",
                attachment_type = allure.attachment_type.PNG
            )






# # conftest.py
# import pytest
# from playwright.sync_api import sync_playwright, Page
#
# @pytest.fixture
# def browser():
#     """每个测试函数独立的浏览器实例"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)  # 有头模式，看得见操作
#         yield browser
#         browser.close()
#
# @pytest.fixture
# def page(browser):
#     """每个测试函数独立的新页面"""
#     context = browser.new_context()
#     page = context.new_page()
#     yield page
#     context.close()
#
# @pytest.fixture
# def logged_in_page(page):
#     """
#     已登录页面 fixture
#     自动完成登录，返回 page 供测试函数使用
#     """
#     page.goto("https://www.saucedemo.com")
#     page.locator("[placeholder='Username']").fill("standard_user")
#     page.locator("[placeholder='Password']").fill("secret_sauce")
#     page.locator("#login-button").click()
#     # 等待登录成功后页面标题出现
#     page.wait_for_selector(".title")
#     return page


# # ========== 核心：失败自动截图 ==========
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """
#     每个用例执行结束后触发。
#     如果是执行阶段(call)且失败了，自动截图并附加到 Allure 报告。
#     """
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == "call" and report.failed:
#         # 从 fixture 中获取 page 对象
#         page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
#         if page:
#             # 截图
#             screenshot = page.screenshot()
#             # 附加到 Allure 报告
#             allure.attach(
#                 screenshot,
#                 name=f"失败截图 - {item.name}",
#                 attachment_type=allure.attachment_type.PNG
#             )
