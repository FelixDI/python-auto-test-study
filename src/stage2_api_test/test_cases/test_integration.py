#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-19 23:25
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_integration.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 端到端集成测试：模拟一个用户从注册到销户的完整生命周期


# pytest src/stage2_api_test/test_cases/ -v --html=reports/stage2_final_report.html --self-contained-html


import pytest
import requests
import time

class TestUserJourney:
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        unique_id = int(time.time_ns())
        self.username = f"journey_{unique_id}"
        self.password = "123456"
        self.email = f"journey_{unique_id}@test.com"
        self.base_url = base_url


    def test_user_full_lifecycle(self):
        register_payload = {
            "username":self.username,
            "password":self.password,
            "email":self.email,
        }

        resp = requests.post(f"{self.base_url}/register",json=register_payload)
        assert resp.status_code == 200,f"注册失败:{resp.text}"
        user_data = resp.json()
        user_id = user_data["id"]
        assert user_data["username"] == self.username

        login_payload = {"username":self.username,"password":self.password}
        resp = requests.post(f"{self.base_url}/login",data=login_payload)
        assert resp.status_code == 200,f"登录失败:{resp.text}"
        token = resp.json()["access_token"]
        headers = {"Authorization":f"Bearer {token}"}

        resp = requests.get(f"{self.base_url}/users/me",headers=headers)
        assert resp.status_code == 200
        me = resp.json()
        assert me["username"] == self.username
        assert me["email"] == self.email

        new_email = f"update_{self.email}"
        update_payload = {
            "username":self.username,
            "password":"newpassword",
            "email":new_email,
        }
        resp = requests.put(f"{self.base_url}/users/{user_id}",json=update_payload,headers=headers)
        assert resp.status_code == 200
        update_user = resp.json()
        assert update_user["email"] == new_email

        resp = requests.post(f"{self.base_url}/login",data=login_payload)
        assert resp.status_code == 401,"旧密码 应该登录失败"

        resp = requests.delete(f"{self.base_url}/users/{user_id}",headers=headers)
        assert resp.status_code == 200
        assert "用户删除成功" in resp.json()["message"]


        resp = requests.get(f"{self.base_url}/users/{user_id}",headers=headers)
        assert resp.status_code == 404




# # test_integration.py
# import requests
# import pytest
# import time
#
# class TestUserJourney:
#     """
#     端到端集成测试：模拟一个用户从注册到销户的完整生命周期
#     覆盖：注册 → 登录 → 查看个人信息 → 修改资料 → 删除账户
#     """
#
#     @pytest.fixture(autouse=True)
#     def setup(self, base_url):
#         """为集成测试准备唯一的测试用户数据"""
#         unique_id = int(time.time_ns())
#         self.username = f"journey_{unique_id}"
#         self.password = "123456"
#         self.email = f"journey_{unique_id}@test.com"
#         self.base_url = base_url
#
#     def test_user_full_lifecycle(self):
#         """
#         完整业务流程测试：
#         1. 注册新用户
#         2. 登录获取 Token
#         3. 用 Token 查看自己的信息
#         4. 修改密码/邮箱
#         5. 用旧密码登录应失败
#         6. 删除账户
#         7. 再次获取用户信息应返回 404
#         """
#         # -------- 1. 注册 --------
#         register_payload = {
#             "username": self.username,
#             "password": self.password,
#             "email": self.email,
#         }
#         resp = requests.post(f"{self.base_url}/register", json=register_payload)
#         assert resp.status_code == 200, f"注册失败: {resp.text}"
#         user_data = resp.json()
#         user_id = user_data["id"]
#         assert user_data["username"] == self.username
#
#         # -------- 2. 登录 --------
#         login_payload = {"username": self.username, "password": self.password}
#         resp = requests.post(f"{self.base_url}/login", data=login_payload)
#         assert resp.status_code == 200, f"登录失败: {resp.text}"
#         token = resp.json()["access_token"]
#         headers = {"Authorization": f"Bearer {token}"}
#
#         # -------- 3. 查看个人信息 --------
#         resp = requests.get(f"{self.base_url}/users/me", headers=headers)
#         assert resp.status_code == 200
#         me = resp.json()
#         assert me["username"] == self.username
#         assert me["email"] == self.email
#
#         # -------- 4. 修改资料（全量更新） --------
#         new_email = f"updated_{self.email}"
#         update_payload = {
#             "username": self.username,
#             "password": "newpassword",
#             "email": new_email,
#         }
#         resp = requests.put(
#             f"{self.base_url}/users/{user_id}",
#             json=update_payload,
#             headers=headers,
#         )
#         assert resp.status_code == 200
#         updated_user = resp.json()
#         assert updated_user["email"] == new_email
#
#         # -------- 5. 用旧密码登录应失败 --------
#         resp = requests.post(
#             f"{self.base_url}/login",
#             data={"username": self.username, "password": self.password},  # 旧密码
#         )
#         assert resp.status_code == 401, "旧密码应该登录失败"
#
#         # -------- 6. 删除账户 --------
#         resp = requests.delete(
#             f"{self.base_url}/users/{user_id}", headers=headers
#         )
#         assert resp.status_code == 200
#         assert "用户删除成功" in resp.json()["message"]
#
#         # -------- 7. 再次获取用户信息应返回 404 --------
#         resp = requests.get(
#             f"{self.base_url}/users/{user_id}", headers=headers
#         )
#         assert resp.status_code == 404