#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-11 08:36
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_user.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 用户模块测试


import pytest


@pytest.mark.smoke
def test_user_register_success_and_password_encrypted(user_api, db_util, test_data):
    new_user = {
        "username": "new_teset_user_20260611",
        "password": "securepass123",
        "email": "new_test@example.com",
    }
    plain_password = new_user["password"]
    response = user_api.register(**new_user)

    # 响应断言
    user_api.assert_status_code(200)  # 基类BaseApi封装三个断言
    user_api.assert_json_contains({
        "username": new_user["username"],
        "email": new_user["email"],
    })
    user_api.assert_json_has_fields(["id"])
    assert "password" not in response.json(), "接口返回了明文密码"

    # 数据库断言
    user_id = response.json()["id"]
    # fixture提供db实例 查询table users，fetchone返回字典  元组参数防注入
    db_user = db_util.query_one(
        "SELECT id, username, email, hashed_password FROM users WHERE id = %s",
        (user_id,)
    )
    assert db_user is not None
    assert db_user["username"] == new_user["username"]
    assert db_user["email"] == new_user["email"]
    assert db_user["hashed_password"] != plain_password, "密码明文存储"  # 虽然命名了hashed_password
    assert db_user["hashed_password"].startswith("$2b$"), "未使用bcrypt加密"
    # assert db_user["hashed_password"] == plain_password, "密码存储错误"   # 实际上后端代码缺陷  明文存储了密码

def test_user_register_duplicate_username(user_api, test_data):
    duplicate_user = {
        "username": "duplicate_test_user",
        "password": "test123",
    }
    first_resp = user_api.register(**duplicate_user)
    user_api.assert_status_code(200)

    second_resp = user_api.register(**duplicate_user)
    user_api.assert_status_code(400)  # 预期错误
    user_api.assert_error_message("用户名已注册")

# @pytest.mark.xfail(reason="已知缺陷：重复邮箱未做业务校验，触发数据库约束返回500")
def test_register_duplicate_email(user_api, test_data):
    user_data = test_data["test_user"]
    user_api.register(**user_data)

    response = user_api.register(
        username = "another_user",
        password = "another_pass",
        email = user_data["email"]
    )
    # user_api.assert_status_code(500)  # 实际上这是后端代码缺陷  没有约束重复邮箱 数据库异常没处理报错  应该写捕获异常代码 返回400
    assert user_api.response.status_code == 400, "未捕获数据库异常 反馈提醒邮箱已注册"
    # 期望行为
    # user_api.assert_status_code(400)
    # user_api.assert_error_message("邮箱已注册")

def test_user_login_success(user_api, test_data):
    user_data = test_data["test_user"]

    user_api.register(**user_data)

    # UserApi类login方法只需两个参数
    response = user_api.login(
        username = user_data["username"],
        password = user_data["password"]
    )
    user_api.assert_status_code(200)
    # 基类封装
    user_api.assert_json_has_fields(["access_token", "token_type"])
    assert response.json()["token_type"] == "bearer"
    assert user_api.token is not None

def test_user_login_wrong_password(user_api, test_data):
    user_data = test_data["test_user"]

    user_api.register(**user_data)

    response = user_api.login(
        username = user_data["username"],
        password = "wrong_password_123"
    )
    user_api.assert_status_code(401)  # 预期错误
    user_api.assert_error_message("用户名或密码错误")
    assert user_api.token is None

# 夹具user_api只返回UserApi实例  未进行register自然不存在  直接login报错
def test_user_login_nonexistent_user(user_api, test_data):
    user_data = test_data["invalid_user"]
    response = user_api.login(
        username = user_data["username"],
        password = user_data["password"]
    )
    user_api.assert_status_code(401)
    user_api.assert_error_message("用户名或密码错误")
    assert user_api.token is None

def test_user_register_missing_required_fields(user_api):
    response1 = user_api.register(username=None, password="test123")
    user_api.assert_status_code(422)

    response2 = user_api.register(username="missing_password_user", password=None)
    user_api.assert_status_code(422)

def test_login_response_not_contains_password(user_api, test_data):
    user_api.register(**test_data["test_user"])
    user_data = test_data["test_user"]
    response = user_api.login(
        username = user_data["username"],
        password = user_data["password"]
    )
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

# # 代码练习
# def test_get_user_profile(authenticated_client):
#     resp = authenticated_client.get_profile()
#     assert resp.status_code == 200
#     assert resp.json()["username"] == authenticated_client.username


# # src/ecommerce_api_test/test_cases/test_user.py
# import pytest
#
# @pytest.mark.smoke
# def test_user_register_success_and_password_encrypted(user_api, db_util, test_data):
#     """
#     合并测试：用户注册成功 + 密码加密存储 + 响应安全校验
#     一次性覆盖核心功能和安全要求
#     """
#     # 使用独立的新用户，不与全局测试用户冲突
#     new_user = {
#         "username": "new_test_user_20260611",
#         "password": "securepass123",
#         "email": "new_test@example.com"
#     }
#     plain_password = new_user["password"]
#
#     # 1. 调用注册接口
#     response = user_api.register(**new_user)
#
#     # 2. 响应断言（基础+安全）
#     user_api.assert_status_code(201)
#     user_api.assert_json_contains({
#         "username": new_user["username"],
#         "email": new_user["email"]
#     })
#     user_api.assert_json_has_fields(["id"])
#     assert "password" not in response.json(), "接口返回了明文密码"
#
#     # 3. 数据库断言（核心校验）
#     user_id = response.json()["id"]
#     db_user = db_util.query_one(
#         "SELECT id, username, email, password FROM users WHERE id = %s",
#         (user_id,)
#     )
#
#     assert db_user is not None
#     assert db_user["username"] == new_user["username"]
#     assert db_user["email"] == new_user["email"]
#     assert db_user["password"] != plain_password, "密码明文存储"
#     assert db_user["password"].startswith("$2b$"), "未使用bcrypt加密"
#
#
# def test_user_register_duplicate_username(user_api, test_data):
#     """
#     测试重复注册同一用户名（必须失败）
#     同一测试函数内连续注册两次，不受全局数据库清理影响
#     """
#     duplicate_user = {
#         "username": "duplicate_test_user",
#         "password": "testpass123"
#     }
#
#     # 第一次注册：成功
#     first_response = user_api.register(**duplicate_user)
#     user_api.assert_status_code(201)
#
#     # 第二次注册：失败（用户名已存在）
#     second_response = user_api.register(**duplicate_user)
#     user_api.assert_status_code(400)
#     user_api.assert_error_message("用户名已注册")
#
#
# def test_user_login_success(user_api, test_data):
#     """测试用户登录成功并自动获取Token"""
#     user_data = test_data["test_user"]
#
#     response = user_api.login(
#         username=user_data["username"],
#         password=user_data["password"]
#     )
#
#     user_api.assert_status_code(200)
#     user_api.assert_json_has_fields(["access_token", "token_type"])
#     assert response.json()["token_type"] == "bearer"
#     assert user_api.token is not None
#
#
# def test_user_login_wrong_password(user_api, test_data):
#     """测试使用错误密码登录"""
#     user_data = test_data["test_user"]
#
#     response = user_api.login(
#         username=user_data["username"],
#         password="wrong_password_123"
#     )
#
#     user_api.assert_status_code(401)
#     user_api.assert_error_message("用户名或密码错误")
#     assert user_api.token is None
#
#
# def test_user_login_nonexistent_user(user_api, test_data):
#     """测试登录不存在的用户"""
#     invalid_user = test_data["invalid_user"]
#
#     response = user_api.login(
#         username=invalid_user["username"],
#         password=invalid_user["password"]
#     )
#
#     user_api.assert_status_code(401)
#     user_api.assert_error_message("用户名或密码错误")
#     assert user_api.token is None
#
#
# def test_user_register_missing_required_fields(user_api):
#     """测试注册时缺少必填字段（用户名/密码）"""
#     # 缺少用户名
#     response1 = user_api.register(username=None, password="testpass123")
#     user_api.assert_status_code(422)
#
#     # 缺少密码
#     response2 = user_api.register(username="missing_pass_user", password=None)
#     user_api.assert_status_code(422)