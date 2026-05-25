#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-25 09:12
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_db.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : practice mysql

import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password="root123",
    database="ecommerce",
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("用户列表:", users)

with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM products WHERE price>%s",(5000,))
    products = cursor.fetchall()
    print("价格>5000的商品:", products)

with conn.cursor() as cursor:
    cursor.execute("INSERT INTO users(username,password,email) VALUES(%s,%s,%s)",
                   ("王五","123456","wangwu@test.com")
    )
    conn.commit()
    print("插入成功, ID:",cursor.lastrowid)

conn.close()
