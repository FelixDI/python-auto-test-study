#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-27 16:47
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_saucedemo_login.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : playwright about web login test

from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # `headless=True`（默认） | 后台运行，看不到浏览器窗口
        page = browser.new_page()

        page.goto("https://saucedemo.com/")

        username_input = page.locator("[placeholder='Username']")
        username_input.fill("standard_user")

        password_input = page.locator("[placeholder='Password']")
        password_input.fill("secret_sauce")

        login_button = page.locator("#login-button")
        login_button.click()

        page.screenshot(path="reports/playwright/saucedemo_after_login.png")

        browser.close()


# # test_saucedemo_login.py
# from playwright.sync_api import sync_playwright
#
# def test_login():
#     """测试 SauceDemo 登录流程：输入用户名、密码，点击登录"""
#     with sync_playwright() as p:
#         # 启动浏览器（有头模式，看到操作过程）
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         # 1. 导航到 SauceDemo
#         page.goto("https://www.saucedemo.com")
#
#         # 2. 定位用户名输入框并输入（通过 placeholder 属性定位）
#         username_input = page.locator("[placeholder='Username']")
#         username_input.fill("standard_user")
#
#         # 3. 定位密码输入框并输入
#         password_input = page.locator("[placeholder='Password']")
#         password_input.fill("secret_sauce")
#
#         # 4. 定位登录按钮并点击（通过 CSS id 定位）
#         login_button = page.locator("#login-button")
#         login_button.click()
#
#         # 5. 截图验证登录后页面
#         page.screenshot(path="reports/playwright/saucedemo_after_login.png")
#
#         # 6. 验证登录成功：检查页面是否包含 "Products" 标题
#         # （第三天会细讲断言，今天先截图确认）
#
#         browser.close()