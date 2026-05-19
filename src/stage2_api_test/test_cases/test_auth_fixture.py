#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 15:15
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_auth_fixture.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : call conftest function

import pytest
import requests
import time

class TestAuth:
    # base_url fixture 自动注入  (conftest.py)
    def test_register_success(self, base_url):
        # unique_id = int(time.time())
        unique_id = int(time.time_ns())
        unique_name = f"testuser_{unique_id}"

        payload = {
            "username":unique_name,
            "password":"123456",
            "email":f"test_{unique_id}@test.com"
        }

        response = requests.post(f"{base_url}/register",json=payload)
        assert response.status_code == 200,f"状态码错误:{response.status_code}"

        data = response.json()
        assert data["username"] == unique_name
        assert data["email"] == f"test_{unique_id}@test.com"
        assert "id" in data

    def test_register_duplicate_fail(self, base_url):
        unique_id = int(time.time())
        unique_name = f"dup_{unique_id}"

        payload = {
            "username":unique_name,
            "password":"123456",
            "email":f"dup_{unique_id}@test.com"
        }

        requests.post(f"{base_url}/register",json=payload)

        response = requests.post(f"{base_url}/register",json=payload)
        assert response.status_code == 400
        assert "用户名已注册" in response.json()["detail"]

    def test_login_success(self, base_url):
        unique_id = int(time.time())
        unique_name = f"login_{unique_id}"

        requests.post(f"{base_url}/register",json={
            "username":unique_name,
            "password":"123456",
            "email":f"login_{unique_id}@test.com"
        })

        payload = {"username":unique_name,"password":"123456"}
        response = requests.post(f"{base_url}/login",data=payload)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, base_url):
        unique_id = int(time.time())
        unique_name = f"wrongpwd_{unique_id}"
        requests.post(f"{base_url}/register",json={
            "username":unique_name,
            "password":"123456",
            "email":f"wrongpwd_{unique_id}@test.com"
        })

        payload = {"username":unique_name,"password":"wrongpassword"}
        response = requests.post(f"{base_url}/login",data=payload)
        assert response.status_code == 401





