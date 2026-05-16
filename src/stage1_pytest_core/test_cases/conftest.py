#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 12:32
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : pytest 实现代码共享和插件化的文件，让 fixture、钩子等可以被同一目录树下的所有测试文件自动发现和使用

import pytest

# 参数默认值scope="function"
@pytest.fixture
def user_data():
    print("\n[前置]准备用户数据")
    data = {"username":"admin", "password":"123456"}
    yield data
    print(" 后置清理用户数据")

@pytest.fixture(scope="class")
def db_connection():
    print("\n[类前置]连接数据库")
    conn = {"db":"test_db", "status":"connected"}
    yield conn
    print("[类后置]关闭数据库连接")

@pytest.fixture(scope="module")
def module_config():
    print("\n[模块前置]加载模块配置")
    yield{"base_url":"http://test.server"}
    print("[模块后置]清理模块配置")


## conftest.py
# import pytest
#
# # ==================== scope="function"（默认，每个用例执行一次） ====================
# @pytest.fixture
# def user_data():
#     """每个测试函数都能拿到独立的用户数据"""
#     print("\n  [前置] 准备用户数据")
#     data = {"username": "admin", "password": "123456"}
#     yield data
#     print("  [后置] 清理用户数据")
#
# # ==================== scope="class"（每个测试类执行一次） ====================
# @pytest.fixture(scope="class")
# def db_connection():
#     """整个测试类共享一个数据库连接"""
#     print("\n[类前置] 连接数据库")
#     conn = {"db": "test_db", "status": "connected"}
#     yield conn
#     print("[类后置] 关闭数据库连接")
#
# # ==================== scope="module"（每个模块执行一次） ====================
# @pytest.fixture(scope="module")
# def module_config():
#     """整个模块共享的配置"""
#     print("\n[模块前置] 加载模块配置")
#     yield {"base_url": "http://test.server"}
#     print("[模块后置] 清理模块配置")

