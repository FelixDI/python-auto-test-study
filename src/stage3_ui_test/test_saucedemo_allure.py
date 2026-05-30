#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-30 16:09
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_saucedemo_allure.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : allure test

import pytest
import allure
from playwright.sync_api import expect

@allure.feature("SauceDemo UI 测试")
class TestSauceDemo:

    @allure.story("登录功能")
    @allure.title("正常登录")
    def test_login_success(self,page):
        with allure.step("打开网站登录页"):
            page.goto("https://saucedemo.com/")

        with allure.step("输入账号密码"):
            page.locator("[placeholder='Username']").fill("standard_user")
            page.locator("[placeholder='Password']").fill("secret_sauce")

        with allure.step("点击登录"):
            page.locator("#login-button").click()

        with allure.step("验证登录成功"):
            expect(page.locator(".title")).to_have_text("Products")


    @allure.story("登录功能")
    @allure.title("密码错误")
    def test_login_failure(self,page):
        with allure.step("打开网站"):
            page.goto("https://saucedemo.com/")

        with allure.step("输入用户和错误密码"):
            page.locator("[placeholder='Username']").fill("standard_user")
            page.locator("[placeholder='Password']").fill("wrong_password")

        with allure.step("点击登录"):
            page.locator("#login-button").click()

        with allure.step("验证错误出现"):
            expect(page.locator("[data-test='error']")).to_be_visible()
            expect(page.locator("[data-test='error']")).to_contain_text(
                "Username and password do not match"
            )

    @allure.story("商品浏览")
    @allure.title("验证商品列表")
    def test_product_count(self,logged_in_page):
        with allure.step("验证页面标题"):
            expect(logged_in_page.locator(".title")).to_have_text("Products")

        with allure.step("断言商品数量为6"):
            expect(logged_in_page.locator(".inventory_item")).to_have_count(6)


# import allure
# from playwright.sync_api import expect
#
#
# @allure.feature("SauceDemo UI 测试")
# class TestSauceDemo:
#
#     @allure.story("登录功能")
#     @allure.title("正常登录——成功进入商品页")
#     def test_login_success(self, page):
#         """登录成功测试"""
#         with allure.step("打开 SauceDemo 登录页"):
#             page.goto("https://www.saucedemo.com")
#
#         with allure.step("输入标准用户名和密码"):
#             page.locator("[placeholder='Username']").fill("standard_user")
#             page.locator("[placeholder='Password']").fill("secret_sauce")
#
#         with allure.step("点击登录按钮"):
#             page.locator("#login-button").click()
#
#         with allure.step("验证登录成功——页面显示 Products 标题"):
#             expect(page.locator(".title")).to_have_text("Products")
#
#     @allure.story("登录功能")
#     @allure.title("登录失败——密码错误")
#     def test_login_failure(self, page):
#         """登录失败测试——会触发失败截图"""
#         with allure.step("打开 SauceDemo 登录页"):
#             page.goto("https://www.saucedemo.com")
#
#         with allure.step("输入正确用户名和错误密码"):
#             page.locator("[placeholder='Username']").fill("standard_user")
#             page.locator("[placeholder='Password']").fill("wrong_password")
#
#         with allure.step("点击登录按钮"):
#             page.locator("#login-button").click()
#
#         with allure.step("验证错误信息出现"):
#             expect(page.locator("[data-test='error']")).to_be_visible()
#             expect(page.locator("[data-test='error']")).to_contain_text(
#                 "Username and password do not match"
#             )
#
#     @allure.story("商品浏览")
#     @allure.title("验证商品列表包含6个商品")
#     def test_product_count(self, logged_in_page):
#         """验证登录后商品数量为6"""
#         with allure.step("验证页面标题"):
#             expect(logged_in_page.locator(".title")).to_have_text("Products")
#
#         with allure.step("断言商品数量为6"):
#             expect(logged_in_page.locator(".inventory_item")).to_have_count(6)