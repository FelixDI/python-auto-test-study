#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 09:07
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : fixture call

import pytest
import requests
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8000"

# @pytest.fixture(autouse=True)
# def clean_database():
#     yield
#
#     engine = create_engine("sqlite:///./test.db",connect_args={"check_same_thread":False})
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     session.execute(text("DELETE FROM users"))
#     session.commit()
#     session.close()


# import pytest
# import requests
# from sqlalchemy import create_engine, text

# ==================== 数据库引擎 ====================
@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False}
    )
    # 核心改动：直接执行SQL建表，不再导入FastAPI模型
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR NOT NULL UNIQUE,
                email VARCHAR NOT NULL UNIQUE,
                hashed_password VARCHAR NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        """))
        conn.commit()
    return engine

# ==================== 数据清理 ====================
@pytest.fixture(autouse=True)
def clean_database(db_engine):
    yield
    # 在测试函数执行后，用 SQL 清空数据
    with db_engine.connect() as conn:
        conn.execute(text("DELETE FROM users"))
        conn.commit()

# ... 其余 fixture (base_url, auth_token, auth_headers) 保持不变 ...



@pytest.fixture(scope="module")
def auth_token(base_url):
    login_data = {
        "username":"apitest",
        "password":"123456"
    }

    requests.post(
        f"{base_url}/register",
        json={
            "username":login_data["username"],
            "password":login_data["password"],
            "email":"apitest@test.com"
        }
    )

    response = requests.post(f"{base_url}/login",data=login_data)
    assert response.status_code == 200,f"模块级账号登录失败:{response.text}"

    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer{auth_token}"}


# import pytest
# import requests
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
#
# # ==================== 管理基础 URL ====================
# @pytest.fixture(scope="module")
# def base_url():
#     """
#     模块级 fixture：提供被测服务的基础地址
#     作用域 scope="module"：整个测试模块只执行一次
#     """
#     return "http://localhost:8000"
#
#
# # ==================== 数据库清理 (解决数据干扰问题) ====================
# @pytest.fixture(autouse=True)
# def clean_database():
#     """
#     自动执行的函数级 fixture
#     核心作用：每次测试结束后，重置数据库，保证测试数据隔离
#     autouse=True 意味着无需在测试函数参数中显式声明，自动生效
#     """
#     # 前置操作 (yield 之前)：测试函数执行前，什么也不做
#     yield
#     # 后置操作 (yield 之后)：测试函数执行后，删除所有用户数据
#     # 连接到容器内的 SQLite 数据库文件
#     engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     # 直接执行 SQL 删除 users 表中的所有数据
#     session.execute(text("DELETE FROM users"))
#     session.commit()
#     session.close()
#
#
# # ==================== 管理登录 Token ====================
# @pytest.fixture(scope="module")
# def auth_token(base_url):
#     """
#     模块级 fixture：登录一次获取 Token，整个模块的测试复用
#     依赖 base_url fixture，pytest 会自动注入它的返回值
#     """
#     login_data = {
#         "username": "apitest",
#         "password": "123456"
#     }
#
#     # 先注册专用测试账号（如果已存在，忽略 400 错误）
#     requests.post(
#         f"{base_url}/register",
#         json={
#             "username": login_data["username"],
#             "password": login_data["password"],
#             "email": "apitest@test.com"
#         }
#     )
#
#     # 登录获取 Token
#     response = requests.post(f"{base_url}/login", data=login_data)
#     # 确保模块级账号登录成功，否则后续测试无法进行
#     assert response.status_code == 200, f"模块级账号登录失败: {response.text}"
#
#     token_data = response.json()
#     # 返回 Token 字符串
#     return token_data["access_token"]
#
#
# # ==================== 为受保护接口准备的请求头 ====================
# @pytest.fixture
# def auth_headers(auth_token):
#     """
#     函数级 fixture：构造携带 Token 的请求头
#     依赖 auth_token fixture，自动获取 Token
#     """
#     return {"Authorization": f"Bearer {auth_token}"}

