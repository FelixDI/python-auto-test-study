#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-19 15:35
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_schema.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : JSON Schema 验证：用 jsonschema 库，适合复杂结构、可复用、报错更清晰  响应断言进阶


import pytest
import requests

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


class TestUserSchema:
    def test_user_me_manual_schema(self, base_url, auth_headers):
        response = requests.get(f"{base_url}/users/me",headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data["id"],int),f"id应为int,实际为{type(data["id"])}"
        assert isinstance(data["username"],str)

        assert data["email"] is None or isinstance(data["email"],str),\
        "email必须是字符串或None"
        assert isinstance(data["is_active"],bool),f"is_active应为bool"

        required_fields = ["id","username","email","is_active"]
        for field in required_fields:
            assert field in data,f"缺少必填字段{field}"

        assert data["is_active"] is True

    def test_users_list_manual_schema(self,base_url,auth_headers):
        response = requests.get(f"{base_url}/users",headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data,list)
        if len(data) > 0:
            user = data[0]
            assert "id" in user
            assert "username" in user
            assert isinstance(user["id"],int)

    @pytest.mark.skipif(not HAS_JSONSCHEMA,reason="未安装jsonschema,跳过")
    def test_user_me_json_schema(self,base_url,auth_headers):
        user_schema = {
            "type":"object",
            "required":["id","username","email","is_active"],
            "properties":{
                "id":{"type":"integer"},
                "username":{"type":"string"},
                "email":{
                    "oneOf":[
                        {"type":"string"},
                        {"type":"null"}
                    ]
                },
                "is_active":{"type":"boolean"}
            }
        }

        response = requests.get(f"{base_url}/users/me",headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        jsonschema.validate(instance=data,schema=user_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA,reason="未安装jsonschema,跳过")
    def test_users_list_json_schema(self,base_url,auth_headers):
        list_schema ={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "username", "email", "is_active"],
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": ["string", "null"]},
                    "is_active": {"type": "boolean"}
                }
            }
        }


        response = requests.get(f"{base_url}/users",headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        jsonschema.validate(instance=data,schema=list_schema)



# import requests
# import pytest
#
# # 如果安装了 jsonschema，则导入；否则跳过相关测试
# try:
#     import jsonschema
#     HAS_JSONSCHEMA = True
# except ImportError:
#     HAS_JSONSCHEMA = False
#
#
# class TestUserSchema:
#     """验证 /users/me 和 /users 接口的响应数据结构"""
#
#     # ---------- 手动断言版本（零依赖） ----------
#     def test_user_me_manual_schema(self, base_url, auth_headers):
#         """
#         手动校验 /users/me 返回的用户对象结构
#         预期字段：id(int), username(str), email(str|None), is_active(bool)
#         """
#         response = requests.get(f"{base_url}/users/me", headers=auth_headers)
#         assert response.status_code == 200
#
#         data = response.json()
#
#         # 1. 验证字段类型
#         assert isinstance(data["id"], int), f"id 应为 int，实际为 {type(data['id'])}"
#         assert isinstance(data["username"], str)
#         # email 可能是 None 或 str
#         assert data["email"] is None or isinstance(data["email"], str), \
#             "email 必须是字符串或 None"
#         assert isinstance(data["is_active"], bool), f"is_active 应为 bool"
#
#         # 2. 验证必填字段存在（没有缺失键）
#         required_fields = ["id", "username", "email", "is_active"]
#         for field in required_fields:
#             assert field in data, f"缺少必填字段: {field}"
#
#         # 3. 验证业务逻辑（is_active 应为 True，因为刚创建的用户是激活的）
#         assert data["is_active"] is True
#
#     def test_users_list_manual_schema(self, base_url, auth_headers):
#         """
#         手动校验 /users 返回的是用户列表，每个元素符合结构
#         """
#         response = requests.get(f"{base_url}/users", headers=auth_headers)
#         assert response.status_code == 200
#
#         data = response.json()
#         # 1. 根是列表
#         assert isinstance(data, list), "返回必须是数组"
#
#         # 2. 如果列表非空，检查第一个元素的结构
#         if len(data) > 0:
#             user = data[0]
#             assert "id" in user
#             assert "username" in user
#             assert isinstance(user["id"], int)
#
#     # ---------- JSON Schema 验证版本（更规范，需要 jsonschema 库） ----------
#     @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="未安装 jsonschema，跳过")
#     def test_user_me_json_schema(self, base_url, auth_headers):
#         """
#         使用 JSON Schema 验证 /users/me 的响应结构
#         JSON Schema 是一种标准化的数据描述语言，适合复杂嵌套、可复用
#         """
#         # 定义期望的 JSON Schema
#         user_schema = {
#             "type": "object",
#             "required": ["id", "username", "email", "is_active"],
#             "properties": {
#                 "id": {"type": "integer"},
#                 "username": {"type": "string"},
#                 "email": {
#                     "oneOf": [
#                         {"type": "string"},
#                         {"type": "null"}
#                     ]
#                 },
#                 "is_active": {"type": "boolean"}
#             }
#         }
#
#         response = requests.get(f"{base_url}/users/me", headers=auth_headers)
#         assert response.status_code == 200
#
#         data = response.json()
#         # 用 jsonschema.validate 进行验证，不符合会抛出 jsonschema.ValidationError
#         jsonschema.validate(instance=data, schema=user_schema)
#         # 如果没有异常，说明通过
#
#     @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="未安装 jsonschema，跳过")
#     def test_users_list_json_schema(self, base_url, auth_headers):
#         """
#         JSON Schema 验证 /users 返回的列表结构
#         """
#         list_schema = {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["id", "username", "email", "is_active"],
#                 "properties": {
#                     "id": {"type": "integer"},
#                     "username": {"type": "string"},
#                     "email": {"type": ["string", "null"]},
#                     "is_active": {"type": "boolean"}
#                 }
#             }
#         }
#
#         response = requests.get(f"{base_url}/users", headers=auth_headers)
#         assert response.status_code == 200
#
#         data = response.json()
#         jsonschema.validate(instance=data, schema=list_schema)
