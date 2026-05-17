#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-17 15:47
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_user_api.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : user api test


import pytest



#必记 3 个钩子（按执行顺序）pytest 的所有接口都遵循完全一致的命名和使用规则，所有钩子都是 pytest_xxx 开头
# pytest_configure(config)：全局只执行一次，做所有初始化工作
# pytest_generate_tests(metafunc)：动态生成测试用例
# pytest_runtest_makereport(item, call)：自定义测试报告（后续会讲）      测试结束：pytest_sessionfinish

#钩子写在conftest.py 最好 因为它是 pytest 自动发现的配置文件钩子是全局生效的，写在普通的 test 文件里只会对当前文件生效

# 必记 3 个对象
# config：全局配置对象，存所有全局数据和缓存
# metafunc：测试收集阶段的测试函数元数据
# request：测试运行阶段的测试用例上下文  request 是 pytest 内置 fixture，不是第三方库，不用 import；让夹具获取测试上下文信息（谁调用、在哪调用）；

# 必记 3 个方法
# config.cache.set(key, value) / config.cache.get(key, default)：读写全局缓存
# metafunc.parametrize(argnames, argvalues, ids)：动态参数化
# request.getfixturevalue(fixture_name)：在夹具里动态调用其他夹具（后续会讲）


def pytest_generate_tests(metafunc):
    #pytest 最强大的测试收集阶段钩子
    #metafunc 对象是什么？pytest 自动传给这个钩子的参数，代表当前正在被收集的单个测试函数的所有元数据
    if "test_case" in metafunc.fixturenames:    #这个测试函数声明的所有 fixture 名称列表

        cases = metafunc.config.cache.get("test_cases", None)  #读全局缓存  支持所有 JSON 可序列化类型（字典、列表、字符串、数字
        if cases is None:   #全局只加载一次数据：避免每个测试函数都重复读取文件，大幅提高速度
            data_dir = __import__("pathlib").Path(__file__).parent.parent/"data"
            import json
            with open(data_dir/"test_cases.json") as f:
                cases = json.load(f)

        ids = [c["id"]for c in cases]
        #给这个测试函数动态添加参数化
        metafunc.parametrize("test_case", cases, ids=ids)

def test_login_with_json_data(api_client, test_case):
    case_id = test_case["id"]
    desc = test_case["desc"]
    body = test_case["body"]
    expected = test_case["expected_code"]

    result = api_client.post("/api/login", body)    #FakeApiClient()
    actual = result["code"]

    assert actual == expected, f"[{case_id}]{desc}:期望{expected},实际{actual}"


@pytest.mark.smoke
def test_login_smoke(api_client):
    result = api_client.post("/api/login", {"username":"admin", "password":"123456"})
    assert result["code"] == 200
    assert result["msg"] == "登录成功"

@pytest.mark.regression
def test_login_empty_fields(api_client):
    r1 = api_client.post("/api/login", {"username":"", "password":"123456"})
    assert r1["code"] == 400

    r2 = api_client.post("/api/login", {"username":"admin", "password":""})
    assert r2["code"] == 400

@pytest.mark.slow
def test_brute_force_simulation(api_client):
    for _ in range(10):
        result = api_client.post("/api/login", {"username":"hacker", "password":"wrong"})
        assert result["code"] == 401

def test_missing_required_body(api_client):
    result = api_client.post("/api/login",{})
    assert result["code"] == 400

@pytest.mark.xfail(reason="已知Bug:错误密码应该返回401,当前代码返回了200")
def test_known_bug_wrong_password(api_client):
    result = api_client.post("/api/login",{"username":"admin", "password":"wrong"})
    assert result["code"] == 200


## test_user_api.py
# import pytest
#
# # ==================== 1. 参数化数据驱动（模块2 + 文件I/O） ====================
# def pytest_generate_tests(metafunc):
#     """
#     动态参数化钩子：从 fixture 获取 JSON 数据，自动生成用例
#     避免手动写一堆 pytest.param()
#     """
#     if "test_case" in metafunc.fixturenames:
#         # 从 module 级别的 load_test_cases fixture 拿到数据
#         cases = metafunc.config.cache.get("test_cases", None)
#         if cases is None:
#             data_dir = __import__("pathlib").Path(__file__).parent.parent / "data"
#             import json
#             with open(data_dir / "test_cases.json") as f:
#                 cases = json.load(f)
#         ids = [c["id"] for c in cases]
#         metafunc.parametrize("test_case", cases, ids=ids)
#
# def test_login_with_json_data(api_client, test_case):
#     """
#     来自 JSON 数据驱动的登录测试
#     test_case 包含：id, desc, url, method, body, expected_code
#     """
#     case_id = test_case["id"]
#     desc = test_case["desc"]
#     body = test_case["body"]
#     expected = test_case["expected_code"]
#
#     # 执行
#     result = api_client.post("/api/login", body)
#     actual = result["code"]
#
#     # 断言
#     assert actual == expected, f"[{case_id}] {desc}：期望 {expected}，实际 {actual}"
#
# # ==================== 2. 标记筛选（模块4） ====================
# @pytest.mark.smoke
# def test_login_smoke(api_client):
#     """冒烟：正常登录必须通过"""
#     result = api_client.post("/api/login", {"username": "admin", "password": "123456"})
#     assert result["code"] == 200
#     assert result["msg"] == "登录成功"
#
# @pytest.mark.regression
# def test_login_empty_fields(api_client):
#     """回归：任意空字段返回 400"""
#     # 用户名为空
#     r1 = api_client.post("/api/login", {"username": "", "password": "123456"})
#     assert r1["code"] == 400
#     # 密码为空
#     r2 = api_client.post("/api/login", {"username": "admin", "password": ""})
#     assert r2["code"] == 400
#
# @pytest.mark.slow
# def test_brute_force_simulation(api_client):
#     """模拟暴力破解检测（耗时标记）"""
#     for _ in range(10):
#         result = api_client.post("/api/login", {"username": "hacker", "password": "wrong"})
#         assert result["code"] == 401
#
# # ==================== 3. 异常断言 + skip/xfail（模块4） ====================
# def test_missing_required_body(api_client):
#     """请求体为空时，预期抛出异常或返回错误"""
#     result = api_client.post("/api/login", {})
#     assert result["code"] == 400
#
# @pytest.mark.xfail(reason="已知 Bug：错误密码应该返回 401，当前代码返回了 200")
# def test_known_bug_wrong_password(api_client):
#     """演示 xfail：这是已知 bug，预期会失败"""
#     result = api_client.post("/api/login", {"username": "admin", "password": "wrong"})
#     assert result["code"] == 401  # 实际 api_client 是对的，这里故意演示 xfail




