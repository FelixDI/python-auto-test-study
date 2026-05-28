#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-28 14:49
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_saucedemo_flow.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 用 Playwright + pytest 对 SauceDemo 完成一个完整的 UI 测试套件

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("SauceDemo电商UI测试")
class TestSauceDemoFlow:

    @allure.story("登录功能")
    @allure.title("正常登录")
    def test_login_success(self,page):
        page.goto("https://saucedemo.com/")
        page.locator("[placeholder='Username']").fill("standard_user")
        page.locator("[placeholder='Password']").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page.locator(".title")).to_have_text("Products")


    @allure.story("登录功能")
    @allure.title("密码错误")
    def test_login_wrong_password(self,page):
        page.goto("https://saucedemo.com/")
        page.locator("[placeholder='Username']").fill("standard_user")
        page.locator("[placeholder='Password']").fill("wrong_password")
        page.locator("#login-button").click()
# 元素的文本包含, 错误提示完整文本是 "Epic sadface: Username and password do not match any user..."
        expect(page.locator("[data-test='error']")).to_contain_text(
            "Username and password do not match"
        )



    @allure.story("商品浏览")
    @allure.title("商品列表")
    def test_product_list_display(self,logged_in_page):
        expect(logged_in_page.locator(".title")).to_have_text("Products")  #元素的完整文本必须完全等于 "Products"
        expect(logged_in_page.locator(".inventory_item")).to_have_count(6)

    @allure.story("商品浏览")
    @allure.title("按价格从低到高排序")
    def test_sort_by_price_low_to_high(self,logged_in_page):
        page = logged_in_page

        page.locator("[data-test='product-sort-container']").select_option("lohi")

        price = page.locator(".inventory_item_price").all_text_contents()
        price_float = [float(p.replace("$","")) for p in price]

        assert price_float == sorted(price_float),f"价格未按升序排列：{price_float}"


    @allure.story("购物车")
    @allure.title("添加商品到购物车并验证数量")
    def test_add_to_cart(self,logged_in_page):
        page = logged_in_page

        page.locator(".inventory_item button").first.click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")
        page.locator(".inventory_item button").nth(1).click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("2")

    @allure.story("购物车")
    @allure.title("购物车页面验证商品信息")
    def test_cart_page(self,logged_in_page):
        page = logged_in_page

        first_item_name = page.locator(".inventory_item_name").first.text_content()
        page.locator(".inventory_item button").first.click()

        page.locator(".shopping_cart_link").click()
        expect(page.locator(".inventory_item_name")).to_have_text(first_item_name)


    @allure.story("结账流程")
    @allure.title("填写信息到完成订单")
    def test_checkout_flow(self,logged_in_page):
        page = logged_in_page

        page.locator(".inventory_item button").first.click()
        page.locator(".shopping_cart_link").click()
        page.locator("#checkout").click()

        page.locator("[placeholder='First Name']").fill("张")
        page.locator("[placeholder='Last Name']").fill("三")
        page.locator("[placeholder='Zip/Postal Code']").fill("230000")
        page.locator("#continue").click()

        expect(page.locator(".summary_info")).to_be_visible()

        page.locator("#finish").click()

        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")

        page.screenshot(path="reports/playwright/saucedemo_order_complete.png")



# # test_saucedemo_flow.py
# import pytest
# import allure
# from playwright.sync_api import expect
#
# @allure.feature("SauceDemo 电商 UI 测试")
# class TestSauceDemoFlow:
#
#     # ==================== 登录 ====================
#     @allure.story("登录功能")
#     @allure.title("正常登录——用户名和密码正确")
#     def test_login_success(self, page):
#         """测试正常登录流程"""
#         page.goto("https://www.saucedemo.com")
#         page.locator("[placeholder='Username']").fill("standard_user")
#         page.locator("[placeholder='Password']").fill("secret_sauce")
#         page.locator("#login-button").click()
#
#         # 断言登录成功——商品标题出现
#         expect(page.locator(".title")).to_have_text("Products")
#
#     @allure.story("登录功能")
#     @allure.title("密码错误——登录失败")
#     def test_login_wrong_password(self, page):
#         """测试错误密码登录"""
#         page.goto("https://www.saucedemo.com")
#         page.locator("[placeholder='Username']").fill("standard_user")
#         page.locator("[placeholder='Password']").fill("wrong_password")
#         page.locator("#login-button").click()
#
#         # 断言错误提示出现
#         expect(page.locator("[data-test='error']")).to_contain_text(
#             "Username and password do not match"
#         )
#
#     # ==================== 商品浏览 ====================
#     @allure.story("商品浏览")
#     @allure.title("商品列表正常展示")
#     def test_product_list_display(self, logged_in_page):
#         """验证登录后能看到商品列表"""
#         # 验证页面标题
#         expect(logged_in_page.locator(".title")).to_have_text("Products")
#         # 验证商品数量为 6
#         expect(logged_in_page.locator(".inventory_item")).to_have_count(6)
#
#     @allure.story("商品浏览")
#     @allure.title("按价格排序——从低到高")
#     def test_sort_by_price_low_to_high(self, logged_in_page):
#         """验证商品排序功能"""
#         page = logged_in_page
#         # 选择排序方式
#         page.locator("[data-test='product-sort-container']").select_option("lohi")
#
#         # 获取所有商品价格
#         prices = page.locator(".inventory_item_price").all_text_contents()
#         # 去掉 $ 符号转浮点数
#         prices_float = [float(p.replace("$", "")) for p in prices]
#         # 断言升序排列
#         assert prices_float == sorted(prices_float), f"价格未按升序排列: {prices_float}"
#
#     # ==================== 购物车 ====================
#     @allure.story("购物车")
#     @allure.title("添加商品到购物车并验证数量")
#     def test_add_to_cart(self, logged_in_page):
#         """测试添加商品到购物车"""
#         page = logged_in_page
#         # 添加第一个商品
#         page.locator(".inventory_item button").first.click()
#         # 验证购物车图标上出现数量 1
#         expect(page.locator(".shopping_cart_badge")).to_have_text("1")
#
#         # 添加第二个商品
#         page.locator(".inventory_item button").nth(1).click()
#         expect(page.locator(".shopping_cart_badge")).to_have_text("2")
#
#     @allure.story("购物车")
#     @allure.title("购物车页面验证商品信息")
#     def test_cart_page(self, logged_in_page):
#         """验证购物车页面中的商品列表"""
#         page = logged_in_page
#         # 添加一个商品
#         first_item_name = page.locator(".inventory_item_name").first.text_content()
#         page.locator(".inventory_item button").first.click()
#         # 进入购物车
#         page.locator(".shopping_cart_link").click()
#         # 验证商品名称一致
#         expect(page.locator(".inventory_item_name")).to_have_text(first_item_name)
#
#     # ==================== 结账流程 ====================
#     @allure.story("结账流程")
#     @allure.title("完整结账流程——填写信息到完成订单")
#     def test_checkout_flow(self, logged_in_page):
#         """测试完整的结账流程"""
#         page = logged_in_page
#         # 1. 添加商品
#         page.locator(".inventory_item button").first.click()
#         # 2. 进入购物车
#         page.locator(".shopping_cart_link").click()
#         # 3. 点击 Checkout
#         page.locator("#checkout").click()
#         # 4. 填写收货信息
#         page.locator("[placeholder='First Name']").fill("张")
#         page.locator("[placeholder='Last Name']").fill("三")
#         page.locator("[placeholder='Zip/Postal Code']").fill("230000")
#         page.locator("#continue").click()
#         # 5. 确认订单
#         expect(page.locator(".summary_info")).to_be_visible()
#         page.locator("#finish").click()
#         # 6. 验证订单完成
#         expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
#         # 7. 截图
#         page.screenshot(path="reports/playwright/saucedemo_order_complete.png")