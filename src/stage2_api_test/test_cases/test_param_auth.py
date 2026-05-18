#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 16:37
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_param_auth.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : parametrize


import pytest
import requests

# 测试数据：用 pytest.param 给每组数据起一个清晰的描述
login_test_data = [
    # 用户名, 密码, 预期状态码, 预期包含的文本, 描述
    pytest.param("testuser", "123456", 200, "access_token", id="正确密码登录"),
    pytest.param("testuser", "wrong", 401, "用户名或密码错误", id="错误密码登录"),
    pytest.param("noexist", "123456", 401, "用户名或密码错误", id="不存在的用户"),
    # 注意：登录接口要求 form-data，用户名密码不能为空，否则返回 422 而非 401
]

@pytest.mark.parametrize("username,password,expected_code,expected_text", login_test_data)
def test_login_param(base_url, username, password, expected_code, expected_text):
    """
    参数化测试登录接口
    前置条件：需要有一个已注册的用户 testuser / 123456
    """
    # 先确保 testuser 这个用户存在（如果已注册会返回 400，忽略）
    requests.post(
        f"{base_url}/register",
        json={"username": "testuser", "password": "123456", "email": "testuser@test.com"}
    )

    # 用参数化的数据发送登录请求
    payload = {"username": username, "password": password}
    response = requests.post(f"{base_url}/login", data=payload)

    # 断言状态码
    assert response.status_code == expected_code, \
        f"{username} 登录：期望 {expected_code}，实际 {response.status_code}"

    # 断言响应体中包含预期文本
    # 如果是 200，检查 token 字段；如果是 401，检查错误信息
    if expected_code == 200:
        assert "access_token" in response.json(), "登录成功但缺少 access_token"
    else:
        assert expected_text in response.json()["detail"], \
            f"错误信息不匹配：{response.json()['detail']}"
