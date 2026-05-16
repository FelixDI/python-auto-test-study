#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 10:42
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_parametrize.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : pytest parametrize

import pytest

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_single_param(user_id):
    assert user_id > 0

@pytest.mark.parametrize("username,password,expected", [
    ("admin","123456", 200),
    ("guest", "guest", 200),
    ("","123456", 400),
    ("admin","", 400),
])
def test_login(username, password, expected):
    if not username or not password:
        actual = 400
    else:
        actual = 200
    assert actual == expected


test_data = [
    {"a":1,"b":2,"expected":3},
    {"a":5,"b":5,"expected":10},
    {"a":0,"b":0,"expected":0},
]

@pytest.mark.parametrize("data", test_data)
def test_add(data):
    assert data["a"]+data["b"] == data["expected"]


@pytest.mark.parametrize("x", [1,2])
@pytest.mark.parametrize("y", [10,20])
def test_multiply(x, y):
    assert x*y in [10, 20, 40]

# pytest.param(参数, id="描述") 给每组数据起个好读的名字
@pytest.mark.parametrize("username,password,expected", [
    pytest.param("admin", "123456", 200, id="正常管理员登录"),
    pytest.param("guest", "guest", 200, id="访客登录"),
    pytest.param("", "123456", 400, id="用户名为空"),
    pytest.param("admin", "", 400, id="密码为空"),
])

def test_login_id(username, password, expected):
    def login(user, pwd):
        if not user or not pwd:
            return 400
        return 200
    assert login(username, password) == expected


# # test_parametrize.py
# import pytest
#
# # ==================== 1. 单参数 ====================
# @pytest.mark.parametrize("user_id", [1, 2, 3])
# def test_single_param(user_id):
#     """一个参数，跑 3 次"""
#     assert user_id > 0
#
# # ==================== 2. 多参数 ====================
# @pytest.mark.parametrize("username,password,expected", [
#     ("admin", "123456", 200),
#     ("guest", "guest", 200),
#     ("", "123456", 400),
#     ("admin", "", 400),
# ])
# def test_login(username, password, expected):
#     """模拟登录：多组数据 → 多条用例"""
#     # 模拟接口调用
#     if not username or not password:
#         actual = 400
#     else:
#         actual = 200
#     assert actual == expected
#
# # ==================== 3. 与已知数据结合（列表/字典） ====================
# test_data = [
#     {"a": 1, "b": 2, "expected": 3},
#     {"a": 5, "b": 5, "expected": 10},
#     {"a": 0, "b": 0, "expected": 0},
# ]
#
# @pytest.mark.parametrize("data", test_data)
# def test_add(data):
#     """传入整个字典"""
#     assert data["a"] + data["b"] == data["expected"]
#
# # ==================== 4. 组合参数化 ====================
# @pytest.mark.parametrize("x", [1, 2])
# @pytest.mark.parametrize("y", [10, 20])
# def test_multiply(x, y):
#     """x=1,2  y=10,20 → 共 4 条用例 (1*10, 1*20, 2*10, 2*20)"""
#     assert x * y in [10, 20, 40]
