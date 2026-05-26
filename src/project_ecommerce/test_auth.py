#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-26 16:28
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_auth.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 用户认证测试

import pytest
import requests
import time
import allure

@allure.feature("用户管理")
class TestAuth:

    @allure.story("用户注册")
    @allure.title("正常注册新用户")
    def test_register_success(self,base_url):
        unique_id = int(time.time_ns())           # time.time() time.time_ns() uuid.uuid4()
        payload = {
            "username":f"testuser_{unique_id}",
            "password":"123456",
            "email":f"test_{unique_id}@test.com"
        }

        with allure.step("发送注册请求"):
            response = requests.post(f"{base_url}/register",json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == payload["username"]

    @allure.story("用户登录")
    @allure.title("正常登录获取Token")
    def test_login_success(self,base_url):
        unique_id = int(time.time_ns())
        username = f"logintest_{unique_id}"
        password = "123456"

        requests.post(f"{base_url}/register",json={
            "username":username,"password":password,
            "email":f"login_{unique_id}@test.com"
        })

        with allure.step("发送登录请求"):
            response = requests.post(f"{base_url}/login",data={
                "username":username,"password":password
            })

            assert response.status_code == 200
            assert "access_token" in response.json()

    @allure.story("用户登录")
    @allure.title("错误密码登录应返回401")
    def test_login_wrong_password(self,base_url):
        unique_id = int(time.time_ns())
        username = f"wrongpwd_{unique_id}"
        requests.post(f"{base_url}/register",json={
            "username":username,"password":"123456",
            "email":f"wrong_{unique_id}@test.com"
        })

        with allure.step("使用错误密码登录"):
            response = requests.post(f"{base_url}/login",data={
                "username":username,"password":"wrongpassword"
            })
            assert response.status_code == 401


# # test_auth.py
# import pytest
# import requests
# import time
# import allure
#
# @allure.feature("用户管理")
# class TestAuth:
#
#     @allure.story("用户注册")
#     @allure.title("正常注册新用户")
#     def test_register_success(self, base_url):
#         unique_id = int(time.time_ns())
#         payload = {
#             "username": f"testuser_{unique_id}",
#             "password": "123456",
#             "email": f"test_{unique_id}@test.com"
#         }
#         with allure.step("发送注册请求"):
#             response = requests.post(f"{base_url}/register", json=payload)
#             assert response.status_code == 200
#             data = response.json()
#             assert data["username"] == payload["username"]
#
#     @allure.story("用户登录")
#     @allure.title("正常登录获取Token")
#     def test_login_success(self, base_url):
#         unique_id = int(time.time_ns())
#         username = f"logintest_{unique_id}"
#         password = "123456"
#         requests.post(f"{base_url}/register", json={
#             "username": username, "password": password,
#             "email": f"login_{unique_id}@test.com"
#         })
#         with allure.step("发送登录请求"):
#             response = requests.post(f"{base_url}/login", data={
#                 "username": username, "password": password
#             })
#             assert response.status_code == 200
#             assert "access_token" in response.json()
#
#     @allure.story("用户登录")
#     @allure.title("错误密码登录应返回401")
#     def test_login_wrong_password(self, base_url):
#         unique_id = int(time.time_ns())
#         username = f"wrongpwd_{unique_id}"
#         requests.post(f"{base_url}/register", json={
#             "username": username, "password": "123456",
#             "email": f"wrong_{unique_id}@test.com"
#         })
#         with allure.step("使用错误密码登录"):
#             response = requests.post(f"{base_url}/login", data={
#                 "username": username, "password": "wrongpassword"
#             })
#             assert response.status_code == 401