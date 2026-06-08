#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-01 12:01
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : login_page.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : login page


"""使用父类封装的方法，实现当前页面 正确访问页面、报错、该页面的所有按钮功能定义,即业务封装类"""

from src.saucedemo_ui_test.common.base_page import BasePage


class LoginPage(BasePage):
    # 元素定位器
    # 实际上就是根据HTML前端代码 来定位
    # 写法	              对应HTML	含义
    # #xxx	              id="xxx"	ID选择器
    # .xxx	            class="xxx"	Class选择器
    # [data-test='xxx']	data-test="xxx"	属性选择器
    USERNAME_INPUT = "#user-name"  # 降低代码耦合度 提高代码可读性 前端代码改动 测试代码不需要改动
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    # 重写父类方法
    def navigate(self):
        super().navigate("")

    # Login场景特殊处理  因为登录会成功或者失败 所有就不return ProductsPage(self.page)
    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)  # BasePage封装的类方法直接用
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)


# # pages/login_page.py
# from src.stage3_ui_test.common.base_page import BasePage
#
# class LoginPage(BasePage):
#     """登录页面"""
#
#     # 元素定位器
#     USERNAME_INPUT = "#user-name"
#     PASSWORD_INPUT = "#password"
#     LOGIN_BUTTON = "#login-button"
#     ERROR_MESSAGE = "[data-test='error']"
#
#     def navigate(self):
#         """导航到登录页面"""
#         super().navigate("")
#
#     def login(self, username: str, password: str):
#         """执行登录操作"""
#         self.fill(self.USERNAME_INPUT, username)
#         self.fill(self.PASSWORD_INPUT, password)
#         self.click(self.LOGIN_BUTTON)
#
#     def get_error_message(self) -> str:
#         """获取登录错误信息"""
#         return self.get_text(self.ERROR_MESSAGE)