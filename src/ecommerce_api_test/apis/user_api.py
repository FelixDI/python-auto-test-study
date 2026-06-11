#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-10 14:26
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : user_api.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 用户管理接口


from src.ecommerce_api_test.common.base_api import BaseApi


class UserApi(BaseApi):
    def register(self, username: str, password: str, email: str = None):
        data = {"username": username, "password": password}
        if email:
            data["email"] = email
        return self.post(endpoint="/register", json=data)

    def login(self, username: str, password: str):
        data = {"username": username, "password": password}
        # FastAPI的OAuth2PasswordRequestForm使用form-data格式
        # json= 会编码成 JSON 请求体，data= 会编码成表单请求体 username=admin&password=123456
        response = self.post(endpoint="/login", data=data)

        if response.status_code == 200:
            token = response.json()["access_token"]
            self.set_auth_token(token)

        return response

    # # 因为fastapi功能有限，下面的接口操作仅作为代码练习 /users/register  /users/login 后端最好都放在/users下
    # def delete_profile(self, username: str):
    #     return self.delete(endpoint="/users/profile/{username}", json={"username": username})
    #
    # def update_profile(self, **kwargs):
    #     return self.put(endpoint="/users/profile", json=kwargs)
    #
    # def get_profile(self):
    #     return self.get(endpoint="/users/profile")
