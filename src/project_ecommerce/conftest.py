#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-25 16:46
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 实战项目夹具集合


import pytest
import pymysql
import allure

@pytest.fixture
def db_connection():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root123",
        database="ecommerce",
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()




