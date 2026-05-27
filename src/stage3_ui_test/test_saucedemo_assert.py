#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-27 17:08
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_saucedemo_assert.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : playwright assert expect

# sync_playwright 内部封装了浏览器通信、自动等待、事件处理等复杂逻辑。
# 调用的 page.goto()、page.locator()、page.click() 这些方法，背后是 Playwright 团队帮你写好了几千行底层代码，你直接拿来用就行。
#
# 这和之前比如 requests.post()、pytest.fixture 一模一样，是官方模块提供的 API。直接提供使用

from playwright.sync_api import sync_playwright,expect

def test_login_and_verify_products_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://saucedemo.com/")

        page.locator("[placeholder='Username']").fill("standard_user")
        page.locator("[placeholder='Password']").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page.locator(".title")).to_have_text("Products")

        page_title = page.text_content(".title")
        print(f"页面标题：{page_title}")
        assert page_title == "Products",f"期望'Products'，实际'{page_title}'"

        cart_icon = page.locator("#shopping_cart_container")
        assert cart_icon.is_visible(),"购物车图标不可见"

        items = page.locator(".inventory_item")
        item_count = items.count()
        print(f"商品数量：{item_count}")
        assert item_count>=1,f"商品数量不足，只有{item_count}个"

        first_item_name = items.first.locator(".inventory_item_name").text_content()
        print(f"第一个商品：{first_item_name}")

        page.screenshot(path="reports/playwright/saucedemo_products.png")

        browser.close()


def test_inventory_item_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://saucedemo.com/")

        page.locator("[placeholder='Username']").fill("standard_user")
        page.locator("[placeholder='Password']").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page.locator(".inventory_item")).to_have_count(6)

        browser.close()


# # test_saucedemo_assert.py
# from playwright.sync_api import sync_playwright, expect
#
# def test_login_and_verify_products_page():
#     """测试登录后进入商品页面，并验证页面内容"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         # 导航到 SauceDemo
#         page.goto("https://www.saucedemo.com")
#
#         # 填写登录信息
#         page.locator("[placeholder='Username']").fill("standard_user")
#         page.locator("[placeholder='Password']").fill("secret_sauce")
#         page.locator("#login-button").click()
#
#         # ---- 断言部分 ----
#
#         # 方式一：expect 自动等待断言（推荐）
#         # 等待 "Products" 标题出现，如果10秒内没出现就报错
#         expect(page.locator(".title")).to_have_text("Products")
#
#         # 方式二：获取文本内容后手动断言
#         page_title = page.text_content(".title")
#         print(f"页面标题: {page_title}")
#         assert page_title == "Products", f"期望 'Products'，实际 '{page_title}'"
#
#         # 验证购物车图标可见
#         cart_icon = page.locator("#shopping_cart_container")
#         assert cart_icon.is_visible(), "购物车图标不可见"
#
#         # 验证商品列表至少有1个商品
#         items = page.locator(".inventory_item")
#         item_count = items.count()
#         print(f"商品数量: {item_count}")
#         assert item_count >= 1, f"商品数量不足，只有 {item_count} 个"
#
#         # 获取第一个商品名称并打印
#         first_item_name = items.first.locator(".inventory_item_name").text_content()
#         print(f"第一个商品: {first_item_name}")
#
#         # 截图
#         page.screenshot(path="reports/playwright/saucedemo_products.png")
#
#         browser.close()
#
# def test_inventory_item_count():
#     """验证商品列表有6个商品"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         page.goto("https://www.saucedemo.com")
#         page.locator("[placeholder='Username']").fill("standard_user")
#         page.locator("[placeholder='Password']").fill("secret_sauce")
#         page.locator("#login-button").click()
#
#         # 使用 expect 断言商品数量
#         expect(page.locator(".inventory_item")).to_have_count(6)
#
#         browser.close()



# pytest 的最佳实践是每个测试函数独立运行，互不干扰。
# 什么时候分开，什么时候合并？
# 场景	                                做法
# 独立的测试场景（登录、购物车、下单）	分开写，失败互不干扰
# 同一个页面的多个验证（标题、商品数、购物车）	合并写，更高效

# 当然，如果想一次打开浏览器，做多个验证，最后再关闭——这完全可行，而且更符合真实用户的操作流程。


# def test_full_flow():
#     """一次打开浏览器，完成登录 + 多个验证"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         # 打开页面
#         page.goto("https://www.saucedemo.com")
#
#         # 登录
#         page.locator("[placeholder='Username']").fill("standard_user")
#         page.locator("[placeholder='Password']").fill("secret_sauce")
#         page.locator("#login-button").click()
#
#         # 验证一：标题
#         expect(page.locator(".title")).to_have_text("Products")
#
#         # 验证二：商品数量
#         expect(page.locator(".inventory_item")).to_have_count(6)
#
#         # 验证三：购物车可见
#         assert page.locator("#shopping_cart_container").is_visible()
#
#         # 截图
#         page.screenshot(path="reports/playwright/saucedemo_full_flow.png")
#
#         # 最后关闭
#         browser.close()
