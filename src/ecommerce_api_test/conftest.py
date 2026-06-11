#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-10 16:04
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 全局夹具


import pytest
import json
import os

from src.ecommerce_api_test.apis.user_api import UserApi
from src.ecommerce_api_test.apis.product_api import ProductApi
from src.ecommerce_api_test.apis.order_api import OrderApi
from src.ecommerce_api_test.utils.db_util import DBUtil


@pytest.fixture(scope="session")
def env_config():
    # Jenkins Pipeline Jenkinsfile: environment {API_BASE_URL = 'http://api:8000' MYSQL_HOST = 'db'}
    return {
        "api_base_url": os.getenv("API_BASE_URL", "http://localhost:8000"),
        "mysql_host": os.getenv("MYSQL_HOST", "localhost"),
        "mysql_port": os.getenv("MYSQL_PORT", "3306"),
        "mysql_user": os.getenv("MYSQL_USER", "root"),
        "mysql_password": os.getenv("MYSQL_PASSWORD", "root123"),
        "mysql_database": os.getenv("MYSQL_DATABASE", "ecommerce")
    }

@pytest.fixture(scope="session")
def db_util(env_config):
    db = DBUtil(
        host=env_config["mysql_host"],
        port=int(env_config["mysql_port"]),  # int
        user=env_config["mysql_user"],
        password=env_config["mysql_password"],
        database=env_config["mysql_database"]
    )
    db.connect()
    print("\n数据库连接成功")

    yield db

    db.close()
    print("\n数据库连接已关闭")

@pytest.fixture(scope="session", autouse=True)
def clean_database_before_test(db_util):
    tables = {"orders", "products", "users"}  # 用order_items存储每个订单的商品明细(商品 ID、购买数量、下单单价)

    db_util.execute("SET FOREIGN_KEY_CHECKS = 0")  # 临时关闭外键约束 允许删除/清空有外键关联的表
    for table in tables:
        db_util.execute(f"TRUNCATE TABLE {table}")  # 快速清空整张表 比 DELETE FROM 更快（直接重置数据页）
    db_util.execute("SET FOREIGN_KEY_CHECKS = 1")

    print("\n数据库清理完成")

@pytest.fixture(scope="session")
def test_data():
    data_file = os.path.join(os.path.dirname(__file__), "data", "test_data.json")

    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

# session 级用于“成本高且无状态/只读资源”，function 级用于“有状态、可能互相影响的测试对象”
@pytest.fixture(scope="function")
def user_api(env_config):
    api = UserApi(base_url=env_config["api_base_url"])
    yield api
    api.close()

# 类比UI测试fixture中的login_page、logged_in_user
@pytest.fixture(scope="session")
def authenticated_client(env_config, test_data):
    user_api = UserApi(base_url=env_config["api_base_url"])

    user_data = test_data["test_user"]
    user_api.register(**user_data)  # 解包字典
    login_resp = user_api.login(user_data["username"], user_data["password"])
    assert login_resp.status_code == 200, "测试用户登录失败"

    token = login_resp.json()["access_token"]
    user_api.set_auth_token(token)
    print("全局测试用户登录成功")

    yield user_api  # return 会结束函数，yield 会暂停函数并返回值，pytest 中利用 yield 实现 setup/teardown 的分离

    user_api.close()

@pytest.fixture(scope="function")
def product_api(env_config, authenticated_client):
    api = ProductApi(base_url=env_config["api_base_url"])
    api.set_auth_token(authenticated_client.token)  # 成功登录的user_api实例调用.token

    yield api

    api.close()

@pytest.fixture(scope="function")
def order_api(env_config, authenticated_client):
    api = OrderApi(base_url=env_config["api_base_url"])
    api.set_auth_token(authenticated_client.token)

    yield api

    api.close()


# # src/ecommerce_api_test/conftest.py
# import pytest
# import json
# import os
# from src.ecommerce_api_test.common.user_api import UserApi
# from src.ecommerce_api_test.common.product_api import ProductApi
# from src.ecommerce_api_test.common.order_api import OrderApi
# from src.ecommerce_api_test.utils.db_util import DBUtil
#
# # --------------------------
# # 核心：环境配置夹具（唯一的配置入口）
# # --------------------------
# @pytest.fixture(scope="session")
# def env_config():
#     """全局唯一的环境配置入口"""
#     return {
#         "api_base_url": os.getenv("API_BASE_URL", "http://localhost:8000"),
#         "mysql_host": os.getenv("MYSQL_HOST", "localhost"),
#         "mysql_port": int(os.getenv("MYSQL_PORT", "3306")),
#         "mysql_user": os.getenv("MYSQL_USER", "root"),
#         "mysql_password": os.getenv("MYSQL_PASSWORD", "root123"),
#         "mysql_database": os.getenv("MYSQL_DATABASE", "ecommerce")
#     }
#
# # --------------------------
# # ✅ 新增：DBUtil夹具（替代之前的db_connection）
# # --------------------------
# @pytest.fixture(scope="session")
# def db_util(env_config):
#     """
#     全局数据库工具夹具
#     整个测试会话只创建一个DBUtil实例
#     所有需要操作数据库的地方都依赖这个夹具
#     """
#     db = DBUtil(
#         host=env_config["mysql_host"],
#         port=env_config["mysql_port"],
#         user=env_config["mysql_user"],
#         password=env_config["mysql_password"],
#         database=env_config["mysql_database"]
#     )
#     db.connect()
#
#     print("\n✅ 数据库连接成功")
#     yield db
#
#     db.close()
#     print("\n✅ 数据库连接已关闭")
#
# # --------------------------
# # 数据库清理夹具（现在依赖db_util）
# # --------------------------
# @pytest.fixture(scope="session", autouse=True)
# def clean_database_before_test(db_util):
#     """测试前自动清理所有测试表"""
#     tables = ["order_items", "orders", "products", "users"]
#
#     db_util.execute("SET FOREIGN_KEY_CHECKS = 0")
#     for table in tables:
#         db_util.execute(f"TRUNCATE TABLE {table}")
#     db_util.execute("SET FOREIGN_KEY_CHECKS = 1")
#
#     print("\n✅ 数据库清理完成")
#
# # --------------------------
# # 其他原有夹具保持不变
# # --------------------------
# @pytest.fixture(scope="session")
# def test_data():
#     data_file = os.path.join(os.path.dirname(__file__), "data", "test_data.json")
#     with open(data_file, "r", encoding="utf-8") as f:
#         return json.load(f)
#
# @pytest.fixture(scope="function")
# def user_api(env_config):
#     api = UserApi(base_url=env_config["api_base_url"])
#     yield api
#     api.close()
#
# @pytest.fixture(scope="session")
# def authenticated_client(env_config, test_data):
#     user_api = UserApi(base_url=env_config["api_base_url"])
#
#     user_data = test_data["test_user"]
#     user_api.register(**user_data)
#     login_resp = user_api.login(user_data["username"], user_data["password"])
#     assert login_resp.status_code == 200
#
#     token = login_resp.json()["access_token"]
#     user_api.set_token(token)
#
#     print("✅ 全局测试用户登录成功")
#     yield user_api
#
#     user_api.close()
#
# @pytest.fixture(scope="function")
# def product_api(env_config, authenticated_client):
#     api = ProductApi(base_url=env_config["api_base_url"])
#     api.set_token(authenticated_client.token)
#     yield api
#     api.close()
#
# @pytest.fixture(scope="function")
# def order_api(env_config, authenticated_client):
#     api = OrderApi(base_url=env_config["api_base_url"])
#     api.set_token(authenticated_client.token)
#     yield api
#     api.close()