#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-25 16:46
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 电商接口测试实战项目夹具


import pytest
import pymysql
import allure
import requests

import os

@pytest.fixture
def db_connection():
    # 如果在 Jenkins 环境里（JENKINS_URL 变量存在），用 Docker 服务名 "db"
    # 否则就是本地开发，用 "localhost"
    if os.environ.get("JENKINS_URL"):
        host = "db"     # docker-compose 中的 mysql 服务名
    else:
        host = "localhost"

    conn = pymysql.connect(
        host=host,
        port=3306,
        user="root",
        password="root123",
        database="ecommerce",
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()


# 测试用例需要调用 FastAPI 接口   pytest测试用例自动获取夹具base_url

@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def auth_token(base_url):
    # import requests
    login_data = {"username":"apitest","password":"123456"}
    requests.post(
        f"{base_url}/register",
        json={
            "username": login_data["username"],
            "password": login_data["password"],
            "email": "apitest@test.com"
        }
    )

    response = requests.post(f"{base_url}/login", data=login_data)
    assert response.status_code == 200,f"模块级账号登录失败：{response.text}"
    # return response.json()["access_token"]
    data = response.json()      # 即使登录返回了 200 但缺少 access_token，也会立刻报错并显示完整的响应内容，方便定位问题
    assert "access_token" in data,f"登录响应缺少 access_token:{data}"
    return data["access_token"]



@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization":f"Bearer {auth_token}"}


# # conftest.py
# import pytest
# import pymysql
# import allure
# import os
#
#
# @pytest.fixture
# def db_connection():
#     if os.environ.get("JENKINS_URL"):
#         host = "db"
#     else:
#         host = "localhost"
#
#     conn = pymysql.connect(
#         host=host,
#         port=3306,
#         user="root",
#         password="root123",
#         database="ecommerce",
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     yield conn
#     conn.close()
#
#
# @pytest.fixture(scope="module")
# def base_url():
#     return "http://localhost:8000"
#
#
# @pytest.fixture(scope="module")
# def auth_token(base_url):
#     import requests
#     login_data = {"username": "apitest", "password": "123456"}
#     requests.post(
#         f"{base_url}/register",
#         json={
#             "username": login_data["username"],
#             "password": login_data["password"],
#             "email": "apitest@test.com"
#         }
#     )
#     response = requests.post(f"{base_url}/login", data=login_data)
#     assert response.status_code == 200, f"模块级账号登录失败: {response.text}"
#     return response.json()["access_token"]
#
#
# @pytest.fixture
# def auth_headers(auth_token):
#     return {"Authorization": f"Bearer {auth_token}"}


