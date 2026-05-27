#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-27 12:34
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_saucedemo.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : playwright+SauceDemo

from playwright.sync_api import sync_playwright

def test_open_saucedemo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://saucedemo.com/")
        title = page.title()
        print(f"页面标题:{title}")
        assert "Swag Labs" in title

        page.screenshot(path="reports/playwright/saucedemo_homepage.png")

        browser.close()

# # test_saucedemo.py
# from playwright.sync_api import sync_playwright
#
# def test_open_saucedemo():
#     """第一个 Playwright 脚本：打开 SauceDemo 首页"""
#     # 启动 Playwright
#     with sync_playwright() as p:
#         # 启动 Chromium 浏览器（有头模式，能看到窗口）
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         # 导航到 SauceDemo
#         page.goto("https://www.saucedemo.com")
#
#         # 获取页面标题并断言
#         title = page.title()
#         print(f"页面标题: {title}")
#         assert "Swag Labs" in title
#
#         # 截图保存
#         page.screenshot(path="reports/saucedemo_homepage.png")
#
#         # 关闭浏览器
#         browser.close()