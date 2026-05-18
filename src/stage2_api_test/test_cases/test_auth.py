#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 09:59
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_auth.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : requests auth test

import pytest
import requests
import time

BASE_URL = "http://localhost:8000"

class TestAuth:

    def test_register_success(self):
        unique_id = int(time.time())

        payload = {
            "username":f"testuser_{unique_id}",
            "password":"123456",
            "email":f"test_{unique_id}@test.com"
        }
        ## 注册测试 → 用新用户名，保证不会被“已存在”干扰payload = {"username": "testuser2", ...}
        # 每运行一次 之前的数据就会让test_register_success报错

        response = requests.post(f"{BASE_URL}/register",json=payload)
        #requests.post() 返回的是一个 Response 对象，它包含了服务器返回的所有信息：
        # response.status_code：HTTP 状态码（200、400、401 等）
        # response.text：原始响应体（字符串）
        # response.json()：把响应体里的 JSON 字符串自动转换成 Python 字典
        #{"id":1,"username":"testuser","email":"test@test.com","is_active":true}

        assert response.status_code == 200,f"状态码错误:{response.status_code}"
        data =response.json()
        assert data["username"] == f"testuser_{unique_id}"
        assert data["email"] == f"test_{unique_id}@test.com"
        assert "id" in data

    def test_register_duplicate_fail(self):
        payload = {
            "username": "testuser",
            "password": "123456",
            "email": "test2@test.com"
        }

        response = requests.post(f"{BASE_URL}/register",json=payload)
        assert response.status_code == 400
        assert "用户名已注册" in response.json()["detail"]

    def test_login_success(self):
        payload = {
            "username":"testuser",
            "password":"123456"
        }

        response = requests.post(f"{BASE_URL}/login",data=payload)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        payload = {
            "username":"testuser",
            "password":"wrongpassword"
        }

        response = requests.post(f"{BASE_URL}/login",data=payload)
        assert response.status_code == 401




# import requests
# import pytest
#
# # 被测服务的基础地址
# BASE_URL = "http://localhost:8000"
#
#
# class TestAuth:
#     """用户认证相关接口测试"""
#
#     def test_register_success(self):
#         """
#         测试：正常注册新用户
#         预期：返回 200，且响应 JSON 中包含正确的 username 和 email
#         """
#         # 请求体：用户名、密码、邮箱 (FastAPI 会自动校验字段类型)
#         payload = {
#             "username": "testuser2",
#             "password": "123456",
#             "email": "test2@test.com"
#         }
#
#         # 发送 POST 请求，json=payload 自动设置 Content-Type 为 application/json
#         response = requests.post(f"{BASE_URL}/register", json=payload)
#
#         # 断言 1：HTTP 状态码必须为 200 (成功)
#         assert response.status_code == 200, f"状态码错误：{response.status_code}"
#
#         # response.json() 将响应体的 JSON 字符串解析为 Python 字典
#         data = response.json()
#
#         # 断言 2：返回的用户名与发送的一致
#         assert data["username"] == "testuser2"
#         # 断言 3：返回的邮箱与发送的一致
#         assert data["email"] == "test2@test.com"
#         # 断言 4：返回数据中必须包含 id 字段 (由数据库自动生成)
#         assert "id" in data
#
#     def test_register_duplicate_fail(self):
#         """
#         测试：重复注册已有用户
#         预期：返回 400，且错误信息中包含"用户名已注册"
#         """
#         payload = {
#             "username": "testuser",   # 这个用户已在上一步成功注册
#             "password": "123456",
#             "email": "test@test.com"
#         }
#
#         response = requests.post(f"{BASE_URL}/register", json=payload)
#
#         # 断言状态码为 400 (客户端错误)
#         assert response.status_code == 400, f"状态码错误：{response.status_code}"
#
#         # FastAPI 的 HTTPException 错误信息会放在 JSON 响应体的 detail 字段里
#         data = response.json()
#         assert "用户名已注册" in data["detail"]
#
#     def test_login_success(self):
#         """
#         测试：用正确密码登录
#         预期：返回 200，且响应中包含 access_token (JWT 令牌)
#         """
#         # 注意：OAuth2PasswordRequestForm 要求用 form-data 格式
#         # 所以这里使用 `data=` 而非 `json=`，requests 会自动处理为表单格式
#         payload = {
#             "username": "testuser",
#             "password": "123456"
#         }
#
#         response = requests.post(f"{BASE_URL}/login", data=payload)
#
#         assert response.status_code == 200
#
#         data = response.json()
#         # access_token 是 JWT 令牌，后续访问受保护接口时需要把它放在请求头里
#         assert "access_token" in data
#         # token_type 固定为 "bearer"
#         assert data["token_type"] == "bearer"
#
#     def test_login_wrong_password(self):
#         """
#         测试：使用错误密码登录
#         预期：返回 401 Unauthorized (未授权)
#         """
#         payload = {
#             "username": "testuser",
#             "password": "wrongpassword"
#         }
#
#         response = requests.post(f"{BASE_URL}/login", data=payload)
#
#         # 密码错误应返回 401 状态码
#         assert response.status_code == 401