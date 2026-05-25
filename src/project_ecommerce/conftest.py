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

import os

@pytest.fixture
def db_connection():
    # 如果在 Jenkins 环境里（JENKINS_URL 变量存在），用 Docker 服务名 "db"
    # 否则就是本地开发，用 "localhost"
    if os.environ.get("JENKINS_URL"):
        host = "db"     # docker-compose 中的 mysql 服务名
    else:
        host = "localhost"

    conn = pymysql.connect(
        host=host,
        port=3306,
        user="root",
        password="root123",
        database="ecommerce",
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()




