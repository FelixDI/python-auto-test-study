#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-29 17:24
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_saucedemo_selenium.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : selenium

# 1. 自动等待机制
# Selenium 需要手动写 WebDriverWait，Playwright 在 click()、fill() 等操作前自动等待元素可见、可交互，代码更简洁，测试更稳定。

# 2. 浏览器上下文
# Playwright 的 browser.new_context() 可以创建独立的浏览器 session，互不干扰。Selenium 没有原生支持，需要手动管理 Cookie。

# 3. 速度
# Playwright 基于 Chrome DevTools Protocol（CDP），比 Selenium 的 HTTP 请求方式更快。

# 4. 多浏览器支持
# Playwright 自带 Chromium、Firefox、WebKit，不需要额外安装驱动。Selenium 需要对应浏览器的驱动文件。

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    _driver = webdriver.Chrome()
    _driver.get("https://www.saucedemo.com")
    yield _driver
    _driver.quit()

def test_login_and_product_count(driver):

    driver.find_element(By.CSS_SELECTOR,"[placeholder='Username']").send_keys("standard_user")
    driver.find_element(By.CSS_SELECTOR,"[placeholder='Password']").send_keys("secret_sauce")
    driver.find_element(By.CSS_SELECTOR,"#login-button").click()

    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"title"))
    )
# 手动写 WebDriverWait判断期望元素出现之后  再继续后面的测试

    items = driver.find_elements(By.CLASS_NAME,"inventory_item")
    assert len(items) == 6,f"期望6个商品,实际{len(items)}个"


def test_login_failure(driver):

    driver.find_element(By.CSS_SELECTOR,"[placeholder='Username']").send_keys("standard_user")
    driver.find_element(By.CSS_SELECTOR,"[placeholder='Password']").send_keys("wrong_password")
    driver.find_element(By.CSS_SELECTOR,"#login-button").click()

    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"[data-test='error']"))
    )

    error_text = driver.find_element(By.CSS_SELECTOR,"[data-test='error']").text
    assert "Username and password do not match" in error_text

# # test_saucedemo_selenium.py
# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# @pytest.fixture
# def driver():
#     """Selenium Chrome 驱动"""
#     _driver = webdriver.Chrome()
#     _driver.get("https://www.saucedemo.com")
#     yield _driver
#     _driver.quit()
#
#
# def test_login_and_product_count(driver):
#     """用 Selenium 验证登录后商品数量为 6"""
#     # 1. 登录
#     driver.find_element(By.CSS_SELECTOR, "[placeholder='Username']").send_keys("standard_user")
#     driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']").send_keys("secret_sauce")
#     driver.find_element(By.CSS_SELECTOR, "#login-button").click()
#
#     # 2. 显式等待商品标题出现（Selenium 需要手动写等待）
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "title"))
#     )
#
#     # 3. 断言商品数量
#     items = driver.find_elements(By.CLASS_NAME, "inventory_item")
#     assert len(items) == 6, f"期望 6 个商品，实际 {len(items)} 个"
#
#
# def test_login_failure(driver):
#     """用 Selenium 验证密码错误时显示错误信息"""
#     driver.find_element(By.CSS_SELECTOR, "[placeholder='Username']").send_keys("standard_user")
#     driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']").send_keys("wrong_password")
#     driver.find_element(By.CSS_SELECTOR, "#login-button").click()
#
#     # 等待错误信息出现
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
#     )
#
#     error_text = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
#     assert "Username and password do not match" in error_text