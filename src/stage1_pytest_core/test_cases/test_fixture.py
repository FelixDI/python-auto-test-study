#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 15:35
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_fixture.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : fixture 调用conftest  进行test


import pytest

def test_with_user_data(user_data):
    assert user_data["username"]=="admin"
    assert user_data["password"]=="123456"

def test_without_fixture():
    assert 1+1 == 2

def test_multiple__fixture(user_data,db_connection):
    assert user_data["username"]=="admin"
    assert db_connection["status"]=="connected"

class TestWithClassFixture:
    #[类前置]连接数据库
    def test_class_case1(self, db_connection):
        assert db_connection["db"] == "test_db"

    def test_class_case2(self, db_connection):
        assert db_connection["status"] == "connected"

    def test_class_case3(self, user_data):
        user_data["username"] ="modified"
        assert user_data["username"] == "modified"

    def test_class_case4(self, user_data):
        assert user_data["username"] == "admin"

    # 最后[类后置]关闭数据库连接


