#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-01 10:50
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : base_page.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : POM(页面对象模型page object model)设计模式，模块化思想项目易于维护和扩展，把不同职责的代码拆分到独立模块中，提高代码复用


# PEP8 常用代码规范
# 逗号 ,      后面空格
# 字典、类型注解 :   后面空格
# 赋值号 =     两边空格  （函数调用不需要，注意与函数定义赋值默认值区分）
# 返回箭头 ->  两边空格
# 缩进4空格
# 类名大驼峰
# 函数名下划线
# 类与类之间：2 个空行
# 模块函数之间：2 个空行
# 类内部方法之间：1 个空行
# 模块、类、函数的 """文档字符串"""


"""Page Object基类封装，登录、商品、购物车、结账四个页面对象，常用的通用方法定义"""

from playwright.sync_api import Page, expect, Locator
from typing import Optional


class BasePage:
    """所有页面对象的基类"""

    def __init__(self, page: Page):
    # def __init__(self, playwright_page: Page):
        self.page = page  # 类属性绑定实例page的引用,基类通过self.page使用实例封装好的函数goto()locator()fill()click()等等
        self.base_url = "https://www.saucedemo.com"

    # 不要把组件放在基类 最终发展成上帝类
    #     self._menu = None  #标记为 未创建该组件的状态
    # #
    # #
    # # saucedemo页面对象较少 手动__init__注入菜单组件对象尚且能够应付。数百个页面对象时就是灾难 而且不是所有页面对象都有该组件对象
    # # 最优的方式 应该采用函数调用方式 测试用例真正使用组件时page.menu，才会创建它，避免了不必要的资源消耗
    # # 还能避免页面对象、组件对象出现循环导入import
    # # property属性装饰器 把一个需要执行逻辑的方法伪装成普通属性访问 不需要page.menu()这样调用
    # @property
    # def menu(self):
    #     if not self._menu:
    #         from src.saucedemo_ui_test.components.menu_component import MenuComponent
    #         self._menu = MenuComponent(self.page)
    #     return self._menu

    def navigate(self, path: str = ""):
        self.page.goto(f"{self.base_url}{path}")

    # 元素定位器locator参数
    def click(self, locator: str):
        self.page.locator(locator).click()
    # def click(self, locator: str | Locator):
    #     if isinstance(locator, str):
    #         self.page.locator(locator).click()
    #     else:
    #         locator.click()

    def fill(self, locator: str, value: str):
        self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        # return self.page.locator(locator).text_content().strip()  # strip() 去除字符串两端的xxx
        text = self.page.locator(locator).text_content()
        return text.strip() if text is not None else ""
        # return text.strip() if text else ""

    def get_attribute(self, locator: str, attribute: str = 'data-test') -> Optional[str]:
        return self.page.locator(locator).get_attribute(attribute)  # 获取元素属性
    # locator = "[data-test='add-to-cart-sauce-labs-backpack']"
    # attribute = 'add-to-cart-sauce-labs-backpack'
    # product_id = "sauce-labs-backpack"

    def is_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()

    def assert_text_contains(self, locator: str, expected_text: str):
        expect(self.page.locator(locator)).to_contain_text(expected_text)

    def assert_element_visible(self, locator: str):
        expect(self.page.locator(locator)).to_be_visible()

    def assert_url_contains(self, expected_path: str):
        expect(self.page).to_have_url(f"{self.base_url}{expected_path}")

    # playwright定位元素时智能等待，但URL跳转不属于元素等待
    # 封装此方法适配不同环境、网络波动，地址匹配后再执行后续操作
    def wait_for_url(self, expected_path: str, timeout: int = 5000):
        """等待页面跳转到指定URL"""
        self.page.wait_for_url(f"{self.base_url}{expected_path}", timeout=timeout)

# POM所有页面对象共享同一个 Playwright 的 Page 实例
# 对比线性流程测试代码自己写一个page
# with sync_playwright() as p:
#     page = p.chromium.launch().new_context().new_page()

# 或者 (推荐，能拿到过程中所有对象 有需要时 可以拿来用。 就像pytest-playwright插件一样)
# p = sync_playwright().start()
# browser = p.chromium.launch()
# context = browser.new_context()
# page = context.new_page()

# 安装playwright 可以手动创建一个实例page = p.chromium.launch().new_page() (不建议这种简写)
# 等价于 page = p.chromium.launch().new_context().new_page() playwright内部会自动补上new_context()
# 不手动创建实例的话 就要额外安装pytest-playwright，Page类提供实例page  否则报错  fixture 'page' not found

# # pytest-playwright插件内部代码（简化版）
# import pytest
# from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page
#
# # 1. 最底层：创建Playwright实例（session级，整个测试会话只创建一次）
# @pytest.fixture(scope="session")
# def playwright():
#     with sync_playwright() as p:
#         yield p  # 测试结束后自动关闭Playwright
#
# # 2. 第二层：创建浏览器实例（session级，整个测试会话只启动一次浏览器）
# @pytest.fixture(scope="session")
# def browser(playwright: Playwright):
#     browser = playwright.chromium.launch(headless=True)
#     yield browser  # 测试结束后自动关闭浏览器
#     browser.close()
#
# # 3. 第三层：创建浏览器上下文（function级，每个测试用例一个新上下文）
# @pytest.fixture(scope="function")
# def context(browser: Browser):
#     context = browser.new_context()
#     yield context  # 测试结束后自动关闭上下文
#     context.close()
#
# # 4. 最上层：创建浏览器页面（function级，每个测试用例一个新页面）
# @pytest.fixture(scope="function")
# def page(context: BrowserContext):
#     page = context.new_page()  # 这就是你拿到的page实例！
#     yield page  # 测试结束后自动关闭页面
#     page.close()


# # common/base_page.py
# from playwright.sync_api import Page, expect
# from typing import Optional
#
# class BasePage:
#     """所有页面的基类，封装通用操作和断言"""
#
#     def __init__(self, page: Page):
#         self.page = page
#         self.base_url = "https://www.saucedemo.com"
#
#     def navigate(self, path: str = ""):
#         """导航到指定页面"""
#         self.page.goto(f"{self.base_url}{path}")
#
#     def click(self, locator: str):
#         """点击元素"""
#         self.page.locator(locator).click()
#
#     def fill(self, locator: str, value: str):
#         """填写输入框"""
#         self.page.locator(locator).fill(value)
#
#     def get_text(self, locator: str) -> str:
#         """获取元素文本"""
#         return self.page.locator(locator).text_content().strip()
#
#     def is_visible(self, locator: str) -> bool:
#         """检查元素是否可见"""
#         return self.page.locator(locator).is_visible()
#
#     def assert_text_contains(self, locator: str, expected_text: str):
#         """断言元素包含指定文本"""
#         expect(self.page.locator(locator)).to_contain_text(expected_text)
#
#     def assert_element_visible(self, locator: str):
#         """断言元素可见"""
#         expect(self.page.locator(locator)).to_be_visible()
#
#     def assert_url_contains(self, expected_path: str):
#         """断言URL包含指定路径"""
#         expect(self.page).to_have_url(f"{self.base_url}{expected_path}")
#
#     def wait_for_url(self, expected_path: str, timeout: int = 5000):
#         """等待页面跳转到指定URL"""
#         self.page.wait_for_url(f"{self.base_url}{expected_path}", timeout=timeout)