#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 15:35
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_fixture.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : fixture 调用conftest  进行test


import pytest

def test_with_user_data(user_data):
    assert user_data["username"]=="admin"
    assert user_data["password"]=="123456"

def test_without_fixture():
    assert 1+1 == 2

def test_multiple__fixture(user_data,db_connection):
    assert user_data["username"]=="admin"
    assert db_connection["status"]=="connected"

class TestWithClassFixture:
    #[类前置]连接数据库
    def test_class_case1(self, db_connection):
        assert db_connection["db"] == "test_db"

    def test_class_case2(self, db_connection):
        assert db_connection["status"] == "connected"

    def test_class_case3(self, user_data):
        user_data["username"] ="modified"
        assert user_data["username"] == "modified"

    def test_class_case4(self, user_data):
        assert user_data["username"] == "admin"

    # 最后[类后置]关闭数据库连接



## test_fixture.py
import pytest

# ==================== 1. 基本用法：自动查找 fixture ====================
# def test_with_user_data(user_data):
#     """参数名匹配 conftest.py 里的 user_data fixture"""
#     assert user_data["username"] == "admin"
#     assert user_data["password"] == "123456"
#
# # ==================== 2. 不使用 fixture 的普通测试 ====================
# def test_without_fixture():
#     """不需要前置数据的用例，不写参数即可"""
#     assert 1 + 1 == 2
#
# # ==================== 3. 使用多个 fixture ====================
# def test_multiple_fixtures(user_data, db_connection):
#     """同时使用用户数据和数据库连接"""
#     assert user_data["username"] == "admin"
#     assert db_connection["status"] == "connected"
#
# # ==================== 4. class 级别 fixture ====================
# class TestWithClassFixture:
#     """测试类：共享 db_connection"""
#
#     def test_class_case1(self, db_connection):
#         assert db_connection["db"] == "test_db"
#
#     def test_class_case2(self, db_connection):
#         # 和 case1 用的是同一个连接（因为 scope="class"）
#         assert db_connection["status"] == "connected"
#
#     def test_class_case3(self, user_data):
#         # 这个用的是 function 级别 fixture，每用例独立
#         user_data["username"] = "modified"
#         assert user_data["username"] == "modified"
#
#     def test_class_case4(self, user_data):
#         # 拿到的还是原始值，因为每个用例独立
#         assert user_data["username"] == "admin"

