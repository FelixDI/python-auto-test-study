#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 16:29
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_markers.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : @pytest.mark.xxx

import pytest
import sys

@pytest.mark.smoke
def test_smoke_login():
    assert True

@pytest.mark.smoke
def test_smoke_homepage():
    assert True

@pytest.mark.regression
def test_regression_user_update():
    assert True

@pytest.mark.slow
def test_slow_report():
    assert True


@pytest.mark.smoke
@pytest.mark.regression
def test_smoke_and_regression():
    assert True


@pytest.mark.skip(reason="功能未实现，暂不测试")
def test_unfinished():
    assert False


@pytest.mark.skipif(sys.platform=="darwin", reason="Mac环境下跳过")
def test_skip_on_mac():
    assert True

@pytest.mark.skipif(sys.version_info<(3,10), reason="需要Python3.10+")
def test__require_new_python():
    assert True


@pytest.mark.xfail(reason="已知bug,等待修复")
def test_known_bug():
    assert 1+1 == 3

@pytest.mark.xfail(sys.platform=="darwin", reason="Mac上预期失败")
def test_xfail_on_mac():
    if sys.platform == "darwin":
        raise RuntimeError("Mac上的已知问题")
    assert True

@pytest.mark.xfail(strict=True,reason="必须失败，如果通过了反而报错")
def test_must_fail():
    assert True


## test_markers.py
# import pytest
# import sys
#
# # ==================== 1. 自定义标记 ====================
# @pytest.mark.smoke
# def test_smoke_login():
#     """冒烟测试：核心登录流程"""
#     assert True
#
# @pytest.mark.smoke
# def test_smoke_homepage():
#     """冒烟测试：首页可访问"""
#     assert True
#
# @pytest.mark.regression
# def test_regression_user_update():
#     """回归测试：用户信息修改"""
#     assert True
#
# @pytest.mark.slow
# def test_slow_report():
#     """耗时测试：生成大数据报表"""
#     assert True
#
# # 一条用例可以打多个标记
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_smoke_and_regression():
#     """既是冒烟又是回归"""
#     assert True
#
# # ==================== 2. 跳过测试 ====================
# @pytest.mark.skip(reason="功能未实现，暂不测试")
# def test_unfinished():
#     """这个测试会被跳过"""
#     assert False
#
# @pytest.mark.skipif(sys.platform == "darwin", reason="Mac 环境下跳过")
# def test_skip_on_mac():
#     """在 Mac 上不运行此测试"""
#     assert True
#
# @pytest.mark.skipif(sys.version_info < (3, 10), reason="需要 Python 3.10+")
# def test_requires_new_python():
#     """Python 版本不够就跳过"""
#     assert True
#
# # ==================== 3. 预期失败 ====================
# @pytest.mark.xfail(reason="已知 bug，等待修复")
# def test_known_bug():
#     """这个测试会失败，但标记为预期失败"""
#     assert 1 + 1 == 3  # 故意写错
#
# @pytest.mark.xfail(sys.platform == "darwin", reason="Mac 上预期失败")
# def test_xfail_on_mac():
#     """在 Mac 上预期失败"""
#     if sys.platform == "darwin":
#         raise RuntimeError("Mac 上的已知问题")
#     assert True
#
# @pytest.mark.xfail(strict=True, reason="必须失败，如果通过了反而报错")
# def test_must_fail():
#     """严格模式：测试通过了反而算失败"""
#     assert True  # 这个断言通过了，但因为 strict=True，会被标记为 FAIL




