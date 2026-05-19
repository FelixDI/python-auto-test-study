#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 17:22
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_users_crud.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 覆盖 GET（查询）、PUT（全量更新）、DELETE（删除），以及鉴权和异常断言



import pytest
import requests
import time

class TestUserCRUD:

    @pytest.fixture(autouse=True)
    def setup(self,base_url,auth_headers):
        unique_id = int(time.time())
        self.username = f"cruduser_{unique_id}"
        self.password = "123456"
        self.email = f"crud_{unique_id}@test.com"

        payload = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }

        response = requests.post(f"{base_url}/register",json=payload)
        assert response.status_code == 200,f"注册测试用户失败:{response.text}"
        # print(type(response.text))
        # print(response.text)       # 多用打印学习与调试，哈哈
        # print(type(response.json()))
        # print(response.json())
        self.user_id = response.json()["id"]
        self.base_url = base_url
        self.headers = auth_headers

        yield

        requests.delete(f"{base_url}/users/{self.user_id}",headers=self.headers)    # headers=auth_headers


    def test_get_all_users(self):
        response = requests.get(f"{self.base_url}/users",headers=self.headers)
        assert response.status_code == 200
        data =response.json()
        assert isinstance(data,list)
        usernames = [u["username"]for u in data]
        assert self.username in usernames

    def test_get_single_user_success(self):
        response = requests.get(f"{self.base_url}/users/{self.user_id}",headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.user_id
        assert data["username"] == self.username

    def test_get_user_not_found(self):
        response = requests.get(f"{self.base_url}/users/99999",headers=self.headers)
        assert response.status_code == 404
        # print("打印看看",response.json())
        assert "用户不存在" in response.json()["detail"]

    def test_get_me_with_token(self):
        response = requests.get(f"{self.base_url}/users/me",headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "apitest"

    def test_get_me_without_token(self):
        response = requests.get(f"{self.base_url}/users/me")
        assert response.status_code == 401

    def test_get_me_with_invalid_token(self):
        response = requests.get(f"{self.base_url}/users/me",headers={"Authorization":"Bearer invalid_token"})
        assert response.status_code == 401


    def test_update_user_success(self):
        new_data = {
            "username":f"updated_{self.username}",
            "password":"newpassword",
            "email":f"updated_{self.username}@test.com"
        }

        response = requests.put(f"{self.base_url}/users/{self.user_id}",json=new_data,headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == new_data["username"]
        assert data["email"] == new_data["email"]

    def test_update_user_no_auth(self):
        response = requests.put(
            f"{self.base_url}/users/{self.user_id}",
            json={"username":"x","password":"x","email":"x@x.com"}
        )



    def test_delete_user_no_auth(self):
        response = requests.delete(f"{self.base_url}/users/{self.user_id}")
        assert response.status_code == 401


    def test_delete_user_success(self):
        temp_id = int(time.time())       # uuid.uuid4()更安全
        temp_user = {
            "username":f"temp_{temp_id}",
            "password":"123456",
            "email":f"temp_{temp_id}@test.com"
        }

        create_resp = requests.post(f"{self.base_url}/register",json=temp_user)
        assert create_resp.status_code == 200
        temp_user_id = create_resp.json()["id"]

        response = requests.delete(f"{self.base_url}/users/{temp_user_id}",headers=self.headers)
        assert response.status_code == 200
        assert "用户删除成功" in response.json()["message"]

        get_resp = requests.get(f"{self.base_url}/users/{temp_user_id}",headers=self.headers)
        assert get_resp.status_code == 404




#
# # test_users_crud.py
# import pytest
# import requests
# import time
#
# class TestUserCRUD:
#     """用户管理接口的增删改查测试（需要 Token 鉴权）"""
#
#     @pytest.fixture(autouse=True)
#     def setup(self, base_url, auth_headers):
#         """每个测试前置：创建一个专属测试用户，并记录其 ID 和用户名"""
#         unique_id = int(time.time())
#         self.username = f"cruduser_{unique_id}"
#         self.password = "123456"
#         self.email = f"crud_{unique_id}@test.com"
#
#         payload = {
#             "username": self.username,
#             "password": self.password,
#             "email": self.email
#         }
#         # 创建用户
#         response = requests.post(f"{base_url}/register", json=payload)
#         assert response.status_code == 200, f"创建测试用户失败: {response.text}"
#         self.user_id = response.json()["id"]
#         self.base_url = base_url
#         self.headers = auth_headers
#
#         yield  # 测试执行
#
#         # 后置清理：通过 API 删除这个测试用户（需要 Token）
#         requests.delete(f"{base_url}/users/{self.user_id}", headers=auth_headers)
#
#     # ---------- GET 查询 ----------
#     def test_get_all_users(self):
#         """GET /users：查询用户列表，应包含分页参数"""
#         response = requests.get(f"{self.base_url}/users", headers=self.headers)
#         assert response.status_code == 200
#         data = response.json()
#         assert isinstance(data, list)
#         # 分页默认 skip=0, limit=100，刚创建的用户应在列表中
#         usernames = [u["username"] for u in data]
#         assert self.username in usernames
#
#     def test_get_single_user_success(self):
#         """GET /users/{id}：查询单个用户，应返回用户信息"""
#         response = requests.get(
#             f"{self.base_url}/users/{self.user_id}",
#             headers=self.headers
#         )
#         assert response.status_code == 200
#         data = response.json()
#         assert data["id"] == self.user_id
#         assert data["username"] == self.username
#
#     def test_get_user_not_found(self):
#         """GET /users/{id}：不存在的用户 ID 应返回 404"""
#         response = requests.get(
#             f"{self.base_url}/users/99999",
#             headers=self.headers
#         )
#         assert response.status_code == 404
#         assert "用户不存在" in response.json()["detail"]
#
#     # ---------- 鉴权测试 ----------
#     def test_get_me_with_token(self):
#         """GET /users/me：携带合法 Token，应返回当前用户信息"""
#         response = requests.get(
#             f"{self.base_url}/users/me",
#             headers=self.headers
#         )
#         assert response.status_code == 200
#         data = response.json()
#         assert data["username"] == "apitest"  # auth_token 是 apitest 的
#
#     def test_get_me_without_token(self):
#         """GET /users/me：不携带 Token，应返回 401"""
#         response = requests.get(f"{self.base_url}/users/me")
#         assert response.status_code == 401
#
#     def test_get_me_invalid_token(self):
#         """GET /users/me：携带无效 Token，应返回 401"""
#         response = requests.get(
#             f"{self.base_url}/users/me",
#             headers={"Authorization": "Bearer invalid_token"}
#         )
#         assert response.status_code == 401
#
#     # ---------- PUT 全量更新 ----------
#     def test_update_user_success(self):
#         """PUT /users/{id}：用合法 Token 更新用户，应成功"""
#         new_data = {
#             "username": f"updated_{self.username}",
#             "password": "newpassword",
#             "email": f"updated_{self.username}@test.com"
#         }
#         response = requests.put(
#             f"{self.base_url}/users/{self.user_id}",
#             json=new_data,
#             headers=self.headers
#         )
#         assert response.status_code == 200
#         data = response.json()
#         assert data["username"] == new_data["username"]
#         assert data["email"] == new_data["email"]
#
#     def test_update_user_no_auth(self):
#         """PUT /users/{id}：无 Token 更新，应返回 401"""
#         response = requests.put(
#             f"{self.base_url}/users/{self.user_id}",
#             json={"username": "x", "password": "x", "email": "x@x.com"}
#         )
#         assert response.status_code == 401
#
#     # ---------- DELETE 删除 ----------
#     def test_delete_user_success(self):
#         """DELETE /users/{id}：用合法 Token 删除用户，应成功"""
#         # 先创建一个临时用户专门用来被删除
#         temp_id = int(time.time())
#         temp_user = {
#             "username": f"temp_{temp_id}",
#             "password": "123456",
#             "email": f"temp_{temp_id}@test.com"
#         }
#         create_resp = requests.post(f"{self.base_url}/register", json=temp_user)
#         assert create_resp.status_code == 200
#         temp_user_id = create_resp.json()["id"]
#
#         # 删除这个用户
#         response = requests.delete(
#             f"{self.base_url}/users/{temp_user_id}",
#             headers=self.headers
#         )
#         assert response.status_code == 200
#         assert "用户删除成功" in response.json()["message"]
#
#         # 再次查询应返回 404
#         get_resp = requests.get(
#             f"{self.base_url}/users/{temp_user_id}",
#             headers=self.headers
#         )
#         assert get_resp.status_code == 404
#
#     def test_delete_user_no_auth(self):
#         """DELETE /users/{id}：无 Token 删除，应返回 401"""
#         response = requests.delete(
#             f"{self.base_url}/users/{self.user_id}"
#         )
#         assert response.status_code == 401