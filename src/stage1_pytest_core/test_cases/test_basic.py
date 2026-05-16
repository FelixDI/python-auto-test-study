#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-15 22:14
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_basic.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : pytest assert/raise

# 核心命令行速记
# pytest               # 运行所有测试
# pytest -v            # 详细模式（看具体哪个测试通过/失败）
# pytest -k "name"     # 运行名称匹配的测试（模糊匹配）
# pytest -x            # 第一次失败后立即停止
# pytest --maxfail=3   # 失败3次后停止
# pytest -m "marker"   # 运行带标记的测试（如 @pytest.mark.slow）


import pytest

def test_math():
    assert 1+1 == 2
    assert 2*3 == 6

def test_string():
    assert "hello".upper() == "HELLO"
    assert "test" in "this is a test"

def test_list():
    nums = [1, 2, 3]
    assert len(nums) == 3
    assert nums[0] == 1

def test_dict():
    resp = {"code": 200, "data":{"name":"admin"}}
    assert resp["code"] == 200
    assert resp["data"]["name"] == "admin"

def test_type_error():
    with pytest.raises(TypeError):
        1 + "2"

def test_value_error_with_match():
    with pytest.raises(ValueError, match="invalid literal") as excinfo:
        int("abc")

    assert "invalid literal" in str(excinfo.value)
    # # 方式一：手动断言 (灵活自定义)
    # with pytest.raises(ValueError) as excinfo:
    #     int("abc")
    # assert "invalid literal for int()" in str(excinfo.value)
    #
    # # 方式二：使用 match 参数 (简洁高效)
    # with pytest.raises(ValueError, match="invalid literal for int()"):
    #     int("abc")

def test_expected_exception_passes():
    with pytest.raises(ZeroDivisionError):
        1/0


# # test_basic.py
# import pytest
#
# # ==================== 基本断言 ====================
# def test_math():
#     """数学运算断言"""
#     assert 1 + 1 == 2
#     assert 2 * 3 == 6
#
# def test_string():
#     """字符串断言"""
#     assert "hello".upper() == "HELLO"
#     assert "test" in "this is a test"
#
# def test_list():
#     """列表断言"""
#     nums = [1, 2, 3]
#     assert len(nums) == 3
#     assert nums[0] == 1
#
# def test_dict():
#     """字典断言"""
#     resp = {"code": 200, "data": {"name": "admin"}}
#     assert resp["code"] == 200
#     assert resp["data"]["name"] == "admin"
#
# # ==================== 异常断言 ====================
# def test_type_error():
#     """断言抛出 TypeError"""
#     with pytest.raises(TypeError):
#         1 + "2"   # 整数加字符串会抛 TypeError
#
# def test_value_error_with_match():
#     """断言抛出 ValueError 并匹配异常信息"""
#     with pytest.raises(ValueError, match="invalid literal"):
#         int("abc")
#
# def test_expected_exception_passes():
#     """如果预期异常被抛出，测试通过（这很合理）"""
#     with pytest.raises(ZeroDivisionError):
#         1 / 0    # 抛异常 → 测试通过

