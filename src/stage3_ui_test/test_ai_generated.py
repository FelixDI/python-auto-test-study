#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-28 20:59
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_ai_generated.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : dify + deepseek v4pro   与coze差不多的步骤 搭建工作流 简单实现调用API 按要求生成测试代码

# 系统提示词：
# 你是一个精通 Playwright Python 自动化测试的专家。你的任务是根据用户的需求描述，生成完整、可直接运行的 Playwright Python 脚本。
# 生成脚本必须遵循以下规则：
# 1. 使用 `sync_playwright()` 同步 API。
# 2. 使用 `page.locator()` 定位元素，优先使用 CSS 选择器或文本选择器。
# 3. 操作前不需要显式等待，Playwright 自带自动等待。
# 4. 包含必要的断言（`assert` 或 `expect`）。
# 5. 只输出 Python 代码，不要输出任何解释。
# 6. 如果需求涉及特定网站（如 SauceDemo），使用正确的 URL 和已知的测试账号（standard_user/secret_sauce）。

# 用户提示词：
# 请根据以下需求，生成 Playwright Python 脚本:
# 快捷键"/" 插入用户输入变量requirement

# requirement:  （这里只是简单尝试，企业项目 开始输入可以直接上传各类格式的文件）
# 打开 SauceDemo 网站，用 standard_user 登录，用 Playwright + pytest 对 SauceDemo 完成一个完整的 UI 测试套件，覆盖：
# 登录成功 / 失败
# 商品列表展示
# 商品排序（价格从低到高）
# 添加商品到购物车 + 验证购物车数量
# 购物车页面验证
# 结账流程（填写信息 → 确认订单 → 完成）
# 订单完成页面验证

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong_password"


@pytest.fixture
def browser_context(browser):
    """为每个测试创建新的上下文，确保隔离"""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(browser_context):
    """为每个测试创建新的页面，并打开基础 URL"""
    page = browser_context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()


def login(page: Page, username: str, password: str):
    """登录辅助函数"""
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_login_success(page: Page):
    """登录成功测试"""
    login(page, USERNAME, PASSWORD)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")


def test_login_failure(page: Page):
    """登录失败测试"""
    login(page, USERNAME, WRONG_PASSWORD)
    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match any user")
    expect(page).to_have_url(BASE_URL)  # 仍停留在登录页


def test_product_list_display(page: Page):
    """商品列表展示测试"""
    login(page, USERNAME, PASSWORD)
    items = page.locator(".inventory_item")
    expect(items.first).to_be_visible()
    # 默认应该有至少1个商品 (SauceDemo 有6个)
    assert items.count() >= 1


def test_sort_by_price_low_to_high(page: Page):
    """按价格从低到高排序测试"""
    login(page, USERNAME, PASSWORD)
    # 选择排序方式
    page.locator('[data-test="product-sort-container"]').select_option("lohi")
    # 获取所有商品价格文本并转换为浮点数
    prices = page.locator(".inventory_item_price").all_inner_texts()
    price_values = [float(p.replace("$", "")) for p in prices]
    # 断言升序排列
    assert price_values == sorted(price_values)


def test_add_to_cart_and_badge(page: Page):
    """添加商品到购物车并验证购物车徽章数量"""
    login(page, USERNAME, PASSWORD)
    # 点击第一个商品的“Add to cart”
    add_buttons = page.locator(".btn_inventory")
    add_buttons.first.click()
    # 验证购物车徽章出现并且文本为1
    badge = page.locator(".shopping_cart_badge")
    expect(badge).to_have_text("1")
    # 再添加第二个商品
    add_buttons.nth(1).click()
    expect(badge).to_have_text("2")


def test_cart_page_validation(page: Page):
    """购物车页面验证"""
    login(page, USERNAME, PASSWORD)
    # 添加一个商品
    page.locator(".btn_inventory").first.click()
    # 进入购物车
    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    # 验证商品出现在购物车中
    cart_items = page.locator(".cart_item")
    expect(cart_items).to_have_count(1)
    # 验证有“Remove”按钮
    expect(page.locator(".cart_button")).to_contain_text("Remove")
    # 验证有“Checkout”按钮
    expect(page.locator('[data-test="checkout"]')).to_be_visible()


def test_checkout_process(page: Page):
    """结账流程完整测试"""
    login(page, USERNAME, PASSWORD)
    # 添加一个商品
    page.locator(".btn_inventory").first.click()
    # 进入购物车
    page.locator(".shopping_cart_link").click()
    # 点击结账
    page.locator('[data-test="checkout"]').click()
    # 填写信息
    page.locator('[data-test="firstName"]').fill("John")
    page.locator('[data-test="lastName"]').fill("Doe")
    page.locator('[data-test="postalCode"]').fill("12345")
    # 继续
    page.locator('[data-test="continue"]').click()
    # 确认订单概览页
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    # 完成订单
    page.locator('[data-test="finish"]').click()
    # 验证完成页面
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
    # 验证“Back Home”按钮存在
    expect(page.locator('[data-test="back-to-products"]')).to_be_visible()


